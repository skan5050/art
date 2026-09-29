"""Импорт справочника городов для карты «География наших продаж» (раздел 8.1 ТЗ).

Критерий отбора (подтверждается с Заказчиком до импорта): население от --min-population
(по умолчанию 100 000) включительно, плюс столицы стран и административные центры
регионов первого уровня независимо от порога.

Источники:
  1) По умолчанию — реестр geo/data/cities.csv, собранный скриптом
     tools/build_cities_registry.py из GeoNames (CC BY 4.0) с русскими названиями
     из справочника hflabs/city (Россия) и ручной проверки (остальные страны).
     Описание отбора и числа записей по странам — docs/geography.md.
  2) --geonames-dir — полная выгрузка GeoNames: файлы стран RU.txt, BY.txt, …,
     admin1CodesASCII.txt и alternatenames/RU.txt, … (или alternateNamesV2.txt).
     Центры регионов — по коду объекта PPLA/PPLC, русские названия — isolanguage=ru.

Импорт не создает продаж: отметки продаж выключены. Записи, измененные вручную,
и включенные отметки продаж при повторном импорте не перезаписываются.
Сохраните указание источника: GeoNames, CC BY 4.0 (https://www.geonames.org/).
"""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from geo.models import City

COUNTRIES = {
    "RU": ("Россия", "Russia"), "BY": ("Беларусь", "Belarus"), "KZ": ("Казахстан", "Kazakhstan"),
    "AM": ("Армения", "Armenia"), "AZ": ("Азербайджан", "Azerbaijan"), "GE": ("Грузия", "Georgia"),
    "KG": ("Кыргызстан", "Kyrgyzstan"), "UZ": ("Узбекистан", "Uzbekistan"), "TJ": ("Таджикистан", "Tajikistan"),
    "EE": ("Эстония", "Estonia"),
}
# Центры регионов, которые не являются крупнейшими городами своего региона (для резервного источника).
KNOWN_ADMIN_CENTERS = {
    "RU": {"Khanty-Mansiysk", "Salekhard", "Magas", "Naryan-Mar", "Anadyr", "Gorno-Altaysk", "Birobidzhan"},
    "KZ": {"Taldykorgan", "Turkestan", "Zhezqazghan", "Konayev", "Qonayev"},
    "UZ": {"Nurafshon", "Gulistan", "Navoiy"},
    "GE": {"Zugdidi", "Telavi", "Ozurgeti", "Akhaltsikhe", "Gori", "Mtskheta", "Ambrolauri", "Rustavi"},
    "AM": {"Ashtarak", "Artashat", "Armavir", "Gavarr", "Hrazdan", "Ijevan", "Kapan", "Yeghegnadzor"},
    "EE": {"Haapsalu", "Kärdla", "Jõhvi", "Paide", "Jõgeva", "Rapla", "Rakvere", "Põlva", "Valga", "Viljandi", "Võru", "Kuressaare"},
}
class Command(BaseCommand):
    help = "Импорт справочника городов для карты продаж (GeoNames)"

    def add_arguments(self, parser):
        parser.add_argument("--min-population", type=int, default=100_000)
        parser.add_argument("--countries", default=",".join(COUNTRIES), help="Коды стран через запятую")
        parser.add_argument("--geonames-dir", help="Папка с файлами полной выгрузки GeoNames")
        parser.add_argument("--registry", help="Сохранить итоговый реестр в CSV")
        parser.add_argument("--registry-in", default=str(Path(__file__).resolve().parents[2] / "data" / "cities.csv"),
                            help="Готовый реестр для импорта (по умолчанию geo/data/cities.csv)")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        countries = [c.strip().upper() for c in opts["countries"].split(",") if c.strip()]
        unknown = [c for c in countries if c not in COUNTRIES]
        if unknown:
            raise CommandError(f"Нет русских названий для стран: {unknown}. Добавьте их в COUNTRIES.")
        if opts["geonames_dir"]:
            rows, source = self.from_dump(Path(opts["geonames_dir"]), countries, opts["min_population"]), "GeoNames dump"
        else:
            rows, source = self.from_registry(Path(opts["registry_in"]), countries, opts["min_population"]), "geo/data/cities.csv"

        by_country = defaultdict(int)
        for row in rows:
            by_country[row["country_code"]] += 1
        for code in countries:
            self.stdout.write(f"{COUNTRIES[code][0]}: {by_country[code]}")
        unverified = sum(1 for r in rows if not r["name_ru_verified"])
        self.stdout.write(f"Всего: {len(rows)}. Источник: {source}. Русских названий к проверке: {unverified}.")

        if opts["registry"]:
            with open(opts["registry"], "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["source_id"])
                writer.writeheader()
                writer.writerows(rows)
            self.stdout.write(f"Реестр сохранен: {opts['registry']}")
        if opts["dry_run"]:
            return

        now = timezone.now()
        created = updated = skipped = 0
        for row in rows:
            city = City.objects.filter(source="GeoNames", source_id=row["source_id"]).first()
            if city and city.manually_edited:
                skipped += 1
                continue
            values = {k: v for k, v in row.items() if k != "source_id"}
            values["loaded_at"] = now
            if city is None:
                City.objects.create(source="GeoNames", source_id=row["source_id"], **values)
                created += 1
            else:
                for key, value in values.items():
                    setattr(city, key, value)
                city.save()  # отметки продаж, видимость и подписи не трогаем
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Добавлено: {created}, обновлено: {updated}, пропущено (ручные правки): {skipped}."))

    def base_row(self, code, geonameid, name, lat, lon, population, region, capital, admin_center, name_ru, verified, stat_date=""):
        return {
            "source_id": str(geonameid),
            "country_code": code,
            "country_ru": COUNTRIES[code][0],
            "country_en": COUNTRIES[code][1],
            "region": region,
            "name_ru": name_ru or name,
            "name_en": name,
            "name_source": name,
            "name_ru_verified": verified,
            "latitude": Decimal(str(lat)).quantize(Decimal("0.00001")),
            "longitude": Decimal(str(lon)).quantize(Decimal("0.00001")),
            "population": int(population) if population else None,
            "population_date": stat_date,
            "is_capital": capital,
            "is_admin_center": admin_center,
        }

    def from_registry(self, path, countries, min_pop):
        if not path.exists():
            raise CommandError(f"Нет файла реестра {path}")
        rows = []
        with path.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["country_code"] not in countries:
                    continue
                capital, admin = r["is_capital"] == "1", r["is_admin_center"] == "1"
                pop = int(r["population"] or 0)
                if pop < min_pop and not capital and not admin:
                    continue
                row = self.base_row(r["country_code"], r["source_id"], r["name_en"], r["latitude"], r["longitude"], pop,
                                    r["region"], capital, admin, r["name_ru"], r["name_ru_verified"] == "1",
                                    stat_date=r.get("population_date", ""))
                row["name_source"] = r.get("name_source") or r["name_en"]
                rows.append(row)
        return rows

    def from_dump(self, folder, countries, min_pop):
        admin1 = {}
        codes_file = folder / "admin1CodesASCII.txt"
        if codes_file.exists():
            for line in codes_file.read_text(encoding="utf-8").splitlines():
                parts = line.split("\t")
                if len(parts) >= 2:
                    admin1[parts[0]] = parts[1]
        rows, wanted = [], {}
        for code in countries:
            path = folder / f"{code}.txt"
            if not path.exists():
                raise CommandError(f"Нет файла {path}")
            with path.open(encoding="utf-8") as fh:
                for line in fh:
                    p = line.rstrip("\n").split("\t")
                    if len(p) < 19 or p[6] != "P":
                        continue
                    fcode, pop = p[7], int(p[14] or 0)
                    capital, admin = fcode == "PPLC", fcode in ("PPLA", "PPLC")
                    if fcode in ("PPLH", "PPLX", "PPLQ", "PPLW"):
                        continue  # исторические, районы, заброшенные
                    if pop < min_pop and not capital and not admin:
                        continue
                    wanted[p[0]] = self.base_row(code, p[0], p[1], p[4], p[5], pop, admin1.get(f"{code}.{p[10]}", p[10]),
                                                 capital, admin, "", False, stat_date=f"GeoNames, изм. {p[18]}")
        ru_names = self.load_ru_names(folder, countries, set(wanted))
        for gid, row in wanted.items():
            if gid in ru_names:
                row["name_ru"], row["name_ru_verified"] = ru_names[gid], True
            rows.append(row)
        return sorted(rows, key=lambda r: (r["country_code"], -(r["population"] or 0)))

    def load_ru_names(self, folder, countries, ids):
        files = [folder / "alternatenames" / f"{c}.txt" for c in countries] + [folder / "alternateNamesV2.txt"]
        best = {}
        for path in files:
            if not path.exists():
                continue
            with path.open(encoding="utf-8") as fh:
                for line in fh:
                    p = line.rstrip("\n").split("\t")
                    if len(p) < 4 or p[1] not in ids or p[2] != "ru":
                        continue
                    historic = len(p) > 7 and p[7] == "1"
                    colloquial = len(p) > 6 and p[6] == "1"
                    if historic or colloquial:
                        continue
                    preferred = len(p) > 4 and p[4] == "1"
                    if p[1] not in best or preferred:
                        best[p[1]] = p[3]
        return best
