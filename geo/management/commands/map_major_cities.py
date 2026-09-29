"""Показать на карте продаж города по умолчанию: все центры регионов России и крупные города
России и ближнего зарубежья (более 800 тыс. жителей).

    python manage.py map_major_cities           — включить отметки и обновить численность
    python manage.py map_major_cities --dry-run — только показать список

Список и актуальная численность — в geo/major_cities.py. Города, измененные вручную
в админке, не трогаются. Другие отметки на карте не выключаются.
"""
from django.core.management.base import BaseCommand

from geo.major_cities import MAJOR_CITIES, default_map_cities
from geo.models import City


def apply_major_cities(queryset=None):
    qs = default_map_cities(queryset if queryset is not None else City.objects.all()).filter(
        source="GeoNames", manually_edited=False)
    count = 0
    for city in qs:
        if city.source_id in MAJOR_CITIES:
            city.population, city.population_date = MAJOR_CITIES[city.source_id]
        city.sale_confirmed = city.visible = True
        city.save(update_fields=["population", "population_date", "sale_confirmed", "visible"])
        count += 1
    return count


class Command(BaseCommand):
    help = "Включить на карте центры регионов России и крупные города (более 800 тыс. жителей)"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        found = {c.source_id: c for c in City.objects.filter(source="GeoNames", source_id__in=list(MAJOR_CITIES))}
        for sid, (population, source) in MAJOR_CITIES.items():
            c = found.get(sid)
            if c is None:
                self.stdout.write(self.style.WARNING(f"  нет в справочнике: {sid}"))
                continue
            note = " — изменен вручную, пропущен" if c.manually_edited else ""
            self.stdout.write(f"  {c.country_ru}: {c.name_ru} — {population:,} ({source}){note}".replace(f"{population:,}", f"{population:,}".replace(",", " ")))
        centers = City.objects.filter(country_code="RU", is_admin_center=True).exclude(source_id__in=list(MAJOR_CITIES))
        self.stdout.write(f"  + центры регионов России: {centers.count()}")
        missing = [sid for sid in MAJOR_CITIES if sid not in found]
        if missing:
            self.stdout.write(self.style.WARNING("Сначала загрузите справочник: python manage.py import_cities"))
        if opts["dry_run"]:
            return
        self.stdout.write(self.style.SUCCESS(f"Отметки включены: {apply_major_cities()}"))
