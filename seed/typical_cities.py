"""Типовые городские страницы для городов России с населением от 500 тыс.

Тексты у всех городов одинаковые и отличаются только названием в нужном падеже
(именительный — name, предложный — prep, винительный — acc, родительный — gen).
Падежные формы проверены вручную и записаны явно — склонение не вычисляется автоматически.
Первые 18 городов (Москва … Тюмень) ведутся отдельными авторскими текстами в cities.py.
"""

# source_id, название, английское, «в/во …» (предложный), «в/во …» (винительный), родительный
FORMS = [
    ("482283", "Тольятти", "Togliatti", "в Тольятти", "в Тольятти", "Тольятти"),
    ("554840", "Ижевск", "Izhevsk", "в Ижевске", "в Ижевск", "Ижевска"),
    ("1510853", "Барнаул", "Barnaul", "в Барнауле", "в Барнаул", "Барнаула"),
    ("532096", "Махачкала", "Makhachkala", "в Махачкале", "в Махачкалу", "Махачкалы"),
    ("2023469", "Иркутск", "Irkutsk", "в Иркутске", "в Иркутск", "Иркутска"),
    ("2022890", "Хабаровск", "Khabarovsk", "в Хабаровске", "в Хабаровск", "Хабаровска"),
    ("479123", "Ульяновск", "Ulyanovsk", "в Ульяновске", "в Ульяновск", "Ульяновска"),
    ("2013348", "Владивосток", "Vladivostok", "во Владивостоке", "во Владивосток", "Владивостока"),
    ("468902", "Ярославль", "Yaroslavl", "в Ярославле", "в Ярославль", "Ярославля"),
    ("515003", "Оренбург", "Orenburg", "в Оренбурге", "в Оренбург", "Оренбурга"),
    ("1489425", "Томск", "Tomsk", "в Томске", "в Томск", "Томска"),
    ("1503901", "Кемерово", "Kemerovo", "в Кемерове", "в Кемерово", "Кемерова"),
    ("523750", "Набережные Челны", "Naberezhnye Chelny", "в Набережных Челнах", "в Набережные Челны", "Набережных Челнов"),
    ("1496990", "Новокузнецк", "Novokuznetsk", "в Новокузнецке", "в Новокузнецк", "Новокузнецка"),
    ("500096", "Рязань", "Ryazan", "в Рязани", "в Рязань", "Рязани"),
    ("580497", "Астрахань", "Astrakhan", "в Астрахани", "в Астрахань", "Астрахани"),
    ("511565", "Пенза", "Penza", "в Пензе", "в Пензу", "Пензы"),
    ("535121", "Липецк", "Lipetsk", "в Липецке", "в Липецк", "Липецка"),
    ("579464", "Балашиха", "Balashikha", "в Балашихе", "в Балашиху", "Балашихи"),
    ("548408", "Киров", "Kirov", "в Кирове", "в Киров", "Кирова"),
]

# Тон A — теплый; тон D — деловой.
TEMPLATES = {
    "a": {
        "title_ru": "Картины {prep}",
        "intro_ru": "Подберем картину для дома {prep}: готовую или на заказ, под размер вашей стены.",
        "body_ru": ("Выбираете картину для дома {prep}? В каталоге есть готовые работы и картины на заказ: сюжет, размер и цвета подберем под вашу комнату. "
                    "Пришлите фото стены — подскажем формат.\n\n"
                    "Картину можно отправить {acc} через СДЭК или другую транспортную компанию по согласованию. Стоимость доставки оплачивается отдельно; "
                    "упаковку и срок уточним до отправки. Заказать картину можно из любой точки {gen}."),
        "seo_title_ru": "Картины {prep}",
        "seo_description_ru": "Картины для дома {prep}: готовые работы и картины на заказ. Доставка {acc} через СДЭК или другую ТК по согласованию.",
        "intro_en": "We will help you choose a painting for your home in {en}: ready-made or made to order, sized for your wall.",
        "body_en": ("Choosing a painting for your home in {en}? The catalogue has ready works and paintings made to order: we will match the subject, size and colours to your room. "
                    "Send a photo of the wall and we will suggest a format.\n\n"
                    "The painting can be shipped to {en} via CDEK or another carrier by agreement. Delivery is paid separately; packing and timing are agreed before shipping."),
    },
    "d": {
        "title_ru": "Картины {prep}",
        "intro_ru": "Готовые работы и индивидуальные заказы с получением {prep}.",
        "body_ru": ("## Выбор работы\nВ каталоге представлены готовые произведения и работы на заказ. Размер, сюжет и цветовое решение согласуются под интерьер; "
                    "фото помещения ускоряет согласование.\n\n"
                    "## Доставка\nОтправка {acc} осуществляется через СДЭК или другую транспортную компанию по согласованию. Доставка оплачивается отдельно; "
                    "упаковка, маршрут и срок уточняются до передачи работы перевозчику. Оформить обращение можно из любой точки {gen}."),
        "seo_title_ru": "Картины {prep}",
        "seo_description_ru": "Картины {prep}: готовые произведения и индивидуальные заказы. Доставка {acc} через СДЭК или другую ТК, оплата доставки отдельно.",
        "intro_en": "Ready works and custom commissions with receipt in {en}.",
        "body_en": ("## Choosing a work\nThe catalogue includes ready works and works made to order. Size, subject and colour scheme are agreed for the interior; "
                    "a photo of the room speeds up the agreement.\n\n"
                    "## Delivery\nShipping to {en} is made via CDEK or another carrier by agreement. Delivery is paid separately; packing, route and timing are agreed before handover to the carrier."),
    },
}


def typical_cities(site):
    t = TEMPLATES[site]
    items = []
    for source_id, name, en, prep, acc, gen in FORMS:
        fmt = {"prep": prep, "acc": acc, "gen": gen, "en": en, "name": name}
        item = {"source_id": source_id, "name_ru": name, "name_en": en, "name_in_ru": prep, "to": acc,
                "title_en": f"Paintings in {en}", "seo_title_en": f"Paintings in {en}"}
        for key, text in t.items():
            item[key] = text.format(**fmt)
        items.append(item)
    return items
