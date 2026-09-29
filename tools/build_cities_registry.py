#!/usr/bin/env python3
"""Сборка реестра городов geo/data/cities.csv для карты «География наших продаж».

Источники:
  * GeoNames (через npm-пакет all-the-cities, CC BY 4.0) — ID, координаты, население,
    код объекта (PPLC — столица, PPLA — центр региона 1-го уровня, PPLX — район города).
  * Справочник городов России hflabs/city (CC BY-SA 4.0, https://github.com/hflabs/city) —
    официальное русское написание городов России; сопоставление по координатам и названию.
  * Для остальных стран русские названия проверены вручную (словарь RU_NAMES ниже).

Отбор: население >= 100 000, столицы (PPLC) и центры регионов (PPLA) независимо от порога.
Исключаются районы городов (PPLX), исторические (PPLH) и заброшенные (PPLQ) пункты,
а также записи с явно ошибочным населением.

Запуск (нужен доступ к npm и raw.githubusercontent.com):
    npm i all-the-cities@3.1.0 && node -e "..."   — см. docs/geography.md
    python tools/build_cities_registry.py atc.json hflabs.csv geo/data/cities.csv
"""
import csv
import difflib
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

COUNTRIES = {
    "RU": ("Россия", "Russia"), "BY": ("Беларусь", "Belarus"), "KZ": ("Казахстан", "Kazakhstan"),
    "AM": ("Армения", "Armenia"), "AZ": ("Азербайджан", "Azerbaijan"), "GE": ("Грузия", "Georgia"),
    "KG": ("Кыргызстан", "Kyrgyzstan"), "UZ": ("Узбекистан", "Uzbekistan"), "TJ": ("Таджикистан", "Tajikistan"),
    "EE": ("Эстония", "Estonia"),
}
MIN_POPULATION = 100_000
MIN_SANE_POPULATION = 500  # записи с населением ниже — вероятные ошибки источника

# Русские названия для стран, кроме России (GeoNames ID → название). Проверено вручную;
# для переименованных городов используется действующее название.
RU_NAMES = {
    # Армения
    616052: "Ереван", 616635: "Гюмри", 616530: "Ванадзор", 616629: "Раздан", 174875: "Капан", 616631: "Армавир",
    616599: "Гавар", 174979: "Арташат", 616877: "Аштарак", 616627: "Иджеван", 174710: "Ехегнадзор",
    # Азербайджан (центры районов — регионы 1-го уровня в GeoNames)
    587084: "Баку", 586523: "Гянджа", 584923: "Сумгайыт", 147622: "Ленкорань", 584649: "Евлах", 585514: "Мингечевир",
    147288: "Саатлы", 148565: "Ширван", 147429: "Нахичевань", 585170: "Шеки", 148619: "Агдам", 585915: "Хырдалан",
    587057: "Барда", 584717: "Хачмаз", 147271: "Сальяны", 148290: "Джалилабад", 585152: "Шамкир", 586427: "Геокчай",
    587384: "Агджабеди", 147982: "Имишли", 585156: "Шемаха", 585187: "Сабирабад", 148106: "Физули", 587378: "Агдаш",
    586763: "Шабран", 585225: "Гаджигабул", 585221: "Губа", 585763: "Кюрдамир", 585226: "Газах", 147105: "Шуша",
    147425: "Нефтчала", 584596: "Закатала", 584871: "Тертер", 148340: "Билясувар", 584716: "Гёйгёль", 587361: "Агсу",
    585220: "Гусар", 584791: "Уджар", 148354: "Бейлаган", 148445: "Астара", 586318: "Исмаиллы", 584821: "Товуз",
    587362: "Агстафа", 585227: "Гах", 585231: "Габала", 584586: "Зардоб", 586765: "Дашкесан", 147552: "Масаллы",
    587070: "Белоканы", 586573: "Кедабек", 586268: "Кельбаджар", 148141: "Джебраил", 146901: "Зангилан",
    586430: "Горанбой", 147611: "Лерик", 585400: "Нафталан", 147305: "Губадлы", 585333: "Огуз", 585177: "Самух",
    147774: "Ходжалы", 146969: "Ходжавенд", 146961: "Ярдымлы", 585570: "Гобустан", 147625: "Лачин", 585909: "Хызы",
    # Беларусь
    625144: "Минск", 627907: "Гомель", 625665: "Могилев", 620127: "Витебск", 627904: "Гродно", 629634: "Брест",
    630468: "Бобруйск", 630429: "Барановичи", 630376: "Борисов", 623549: "Пинск", 624079: "Орша", 625324: "Мозырь",
    622428: "Солигорск", 625625: "Молодечно", 624784: "Новополоцк",
    # Эстония
    588409: "Таллин", 588335: "Тарту", 589580: "Пярну", 587577: "Вильянди", 589165: "Раквере", 590939: "Курессааре",
    587450: "Выру", 587876: "Валга", 592225: "Хаапсалу", 591893: "Йыхви", 589709: "Пайде", 589375: "Пылва",
    591902: "Йыгева", 589116: "Рапла", 591632: "Кярдла",
    # Грузия
    611717: "Тбилиси", 613607: "Кутаиси", 615532: "Батуми", 611847: "Сухуми", 610824: "Зугдиди", 612287: "Рустави",
    614455: "Гори", 611694: "Телави", 612536: "Озургети", 615860: "Ахалцихе", 612890: "Мцхета",
    # Кыргызстан
    1528675: "Бишкек", 1527534: "Ош", 1528249: "Джалал-Абад", 1528121: "Каракол", 1527592: "Нарын", 1527299: "Талас",
    1528735: "Баткен",
    # Казахстан
    1526384: "Алматы", 609655: "Караганда", 1518980: "Шымкент", 1516905: "Тараз", 1526273: "Астана", 1520240: "Павлодар",
    1520316: "Усть-Каменогорск", 1519922: "Кызылорда", 1519422: "Семей", 610611: "Актобе", 1519928: "Костанай",
    1520172: "Петропавловск", 608668: "Уральск", 610529: "Атырау", 1518262: "Темиртау", 610612: "Актау",
    1522203: "Кокшетау", 1519843: "Рудный", 1524325: "Экибастуз", 1518542: "Талдыкорган", 1516589: "Жезказган",
    607610: "Жанаозен", 1517945: "Туркестан", 1521368: "Байконур",
    # Таджикистан
    1221874: "Душанбе", 1514879: "Худжанд", 1220747: "Бохтар", 1221328: "Хорог",
    # Узбекистан
    1512569: "Ташкент", 1513157: "Наманган", 1216265: "Самарканд", 1514588: "Андижан", 1217662: "Бухара",
    601294: "Нукус", 1216311: "Карши", 1512979: "Коканд", 1514210: "Чирчик", 1514019: "Фергана", 1513886: "Джизак",
    1512473: "Ургенч", 1215957: "Термез", 1513243: "Маргилан", 1513131: "Навои", 1514581: "Ангрен", 1513064: "Алмалык",
    1513966: "Гулистан",
}
# Районы крупных городов, которые GeoNames отмечает как отдельные пункты (раздел 8.1: районы не включаются).
EXCLUDED_DISTRICTS = {
    "Zelenograd": "административный округ Москвы",
    "Novo-Peredelkino": "район Москвы",
    "Cherëmushki": "район Москвы",
    "Kolpino": "район Санкт-Петербурга",
    "Zheleznodorozhnyy": "вошел в состав Балашихи",
}
RU_NAMES_RUSSIA = {524901: "Москва", 498817: "Санкт-Петербург"}

# Английские названия, устаревшие в GeoNames.
EN_NAMES = {1526273: "Astana", 1220747: "Bokhtar", 586763: "Shabran", 148340: "Bilasuvar", 584716: "Goygol",
            585231: "Gabala", 146969: "Khojavend", 586765: "Dashkasan"}

TRANSLIT = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y",
            "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
            "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya"}


# Центры субъектов РФ, которых нет в выборке GeoNames как PPLA (добавляются вручную).
MANUAL_ROWS = [
    {"source_id": "561887", "country_code": "RU", "region": "Ленинградская обл", "name_ru": "Гатчина", "name_en": "Gatchina",
     "latitude": "59.57639", "longitude": "30.12833", "note": "административный центр Ленинградской области с 2021 г."},
    {"source_id": "542374", "country_code": "RU", "region": "Московская обл", "name_ru": "Красногорск", "name_en": "Krasnogorsk",
     "latitude": "55.82036", "longitude": "37.33017", "note": "место размещения правительства Московской области"},
]


def translit(text):
    return re.sub(r"[^a-z]", "", "".join(TRANSLIT.get(ch, ch) for ch in text.lower()))


def distance_km(lat1, lon1, lat2, lon2):
    p = math.pi / 180
    a = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(a))


def main(atc_path, hflabs_path, out_path):
    cities = json.load(open(atc_path, encoding="utf-8"))
    hflabs = list(csv.DictReader(open(hflabs_path, encoding="utf-8")))
    rows, problems, matched_caps = [], [], set()
    for c in cities:
        code, fcode, pop = c["country"], c["featureCode"], c["population"] or 0
        if code not in COUNTRIES or fcode in ("PPLX", "PPLH", "PPLQ", "PPLW"):
            continue
        capital, admin = fcode == "PPLC", fcode in ("PPLC", "PPLA")
        if not (capital or admin or (pop >= MIN_POPULATION and fcode.startswith("PPL"))):
            continue
        if pop < MIN_SANE_POPULATION:
            problems.append(f"исключено (население {pop}): {code} {c['name']} {c['cityId']}")
            continue
        if code == "RU" and c["name"] in EXCLUDED_DISTRICTS:
            problems.append(f"исключено ({EXCLUDED_DISTRICTS[c['name']]}): {c['name']} {c['cityId']}")
            continue
        lon, lat = c["loc"]["coordinates"]
        region = ""
        if code == "RU":
            near = [h for h in hflabs if distance_km(lat, lon, float(h["geo_lat"]), float(h["geo_lon"])) <= 40]
            best = max(near, key=lambda h: difflib.SequenceMatcher(None, translit(h["city"] or h["area"] or h["region"]), c["name"].lower().replace("-", "").replace(" ", "")).ratio())
            name_ru = best["city"] or best["area"] or best["region"]
            score = difflib.SequenceMatcher(None, translit(name_ru), re.sub(r"[^a-z]", "", c["name"].lower())).ratio()
            if c["cityId"] in RU_NAMES_RUSSIA and name_ru == RU_NAMES_RUSSIA[c["cityId"]]:
                score = 1.0
            dist = distance_km(lat, lon, float(best["geo_lat"]), float(best["geo_lon"]))
            region = f"{best['region']} {best['region_type']}".strip()
            if best["capital_marker"] in ("2", "3"):
                admin = True
                matched_caps.add(best["fias_id"])
            if score < 0.55 or dist > 15:
                problems.append(f"проверить: {c['name']} → {name_ru} (сходство {score:.2f}, {dist:.0f} км)")
            verified = score >= 0.55 and dist <= 15
            note = "hflabs/city"
        else:
            name_ru = RU_NAMES.get(c["cityId"], "")
            verified = bool(name_ru)
            note = "проверено вручную"
            if not name_ru:
                problems.append(f"нет русского названия: {code} {c['name']} {c['cityId']}")
                continue
        rows.append({
            "source_id": c["cityId"], "country_code": code, "country_ru": COUNTRIES[code][0], "country_en": COUNTRIES[code][1],
            "region": region, "name_ru": name_ru, "name_en": EN_NAMES.get(c["cityId"], c["name"]), "name_source": c["name"],
            "name_ru_verified": int(verified), "name_ru_source": note, "latitude": f"{lat:.5f}", "longitude": f"{lon:.5f}",
            "population": pop, "population_date": "GeoNames (дата переписи в источнике не указана)",
            "is_capital": int(capital), "is_admin_center": int(admin), "feature_code": fcode,
        })
    missing_caps = [h["city"] or h["area"] or h["region"] for h in hflabs if h["capital_marker"] in ("2", "3") and h["fias_id"] not in matched_caps]
    for name in missing_caps:
        problems.append(f"центр региона России не найден в GeoNames-выборке: {name}")
    known = {str(r["source_id"]) for r in rows}
    for m in MANUAL_ROWS:
        if m["source_id"] in known:
            continue
        rows.append({
            "source_id": m["source_id"], "country_code": m["country_code"], "country_ru": COUNTRIES[m["country_code"]][0],
            "country_en": COUNTRIES[m["country_code"]][1], "region": m["region"], "name_ru": m["name_ru"], "name_en": m["name_en"],
            "name_source": m["name_en"], "name_ru_verified": 1, "name_ru_source": f"вручную: {m['note']}",
            "latitude": m["latitude"], "longitude": m["longitude"], "population": 0, "population_date": "",
            "is_capital": 0, "is_admin_center": 1, "feature_code": "PPLA",
        })
    # Актуальная численность крупных городов (geo/major_cities.py) вместо устаревшей из GeoNames
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from geo.major_cities import MAJOR_CITIES
    for r in rows:
        if str(r["source_id"]) in MAJOR_CITIES:
            r["population"], r["population_date"] = MAJOR_CITIES[str(r["source_id"])]
    rows.sort(key=lambda r: (list(COUNTRIES).index(r["country_code"]), -int(r["population"] or 0)))
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = {}
    for r in rows:
        counts[r["country_ru"]] = counts.get(r["country_ru"], 0) + 1
    print(f"Сформировано {date.today()}: {len(rows)} записей → {out_path}")
    for name, n in counts.items():
        print(f"  {name}: {n}")
    print("Замечания:")
    for p in problems:
        print("  " + p)


if __name__ == "__main__":
    main(*sys.argv[1:4])
