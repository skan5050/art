"""Демонстрационные картины для локальной проверки верстки.

    python manage.py seed_demo           — создать демо-работы (артикул DEMO-…)
    python manage.py seed_demo --remove  — удалить их

Не используйте на рабочем сайте: демо-работы не являются реальным ассортиментом.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from catalog.models import Category, Painting, PaintingImage, Technique
from geo.models import City

A, S = "available", "sold"
def _rows(site, items):
    return [(c, ru, en, st, f"{n:02d}_{'available' if st == A else 'sold'}_{site}.jpg") for n, (c, ru, en, st) in enumerate(items, 1)]


# 24 тестовые картины заказчика (по 12 на сайт): первые 6 «В наличии», следующие 6 SOLD. Статусы выводит интерфейс.
DEMO_SITES = {
    "a": _rows("MiraMe", [
        ("море", "Солнечный берег", "Sunny shore", A), ("цветы-и-ботаника", "Пионы у окна", "Peonies by the window", A),
        ("город-и-архитектура", "Улица к морю", "The street to the sea", A), ("абстракция", "Воздух и золото", "Air and gold", A),
        ("пейзажи", "Тихая Тоскана", "Quiet Tuscany", A), ("город-и-архитектура", "Вечерний город", "Evening city", A),
        ("натюрморт", "Лимоны и олива", "Lemons and olive", S), ("животные", "Верный друг", "A faithful friend", S),
        ("птицы", "Весенний полёт", "Spring flight", S), ("рыбы", "Подводный свет", "Underwater light", S),
        ("интерьер-и-бытовые-сцены", "Комната у моря", "A room by the sea", S), ("абстракция", "Тёплая геометрия", "Warm geometry", S),
    ]),
    "d": _rows("HolStori", [
        ("абстракция", "Структура I", "Structure I", A), ("море", "Северный свет", "Northern light", A),
        ("цветы-и-ботаника", "Белые цветы", "White flowers", A), ("город-и-архитектура", "После дождя", "After the rain", A),
        ("животные", "Белая лошадь", "White horse", A), ("интерьер-и-бытовые-сцены", "Тихий интерьер", "Quiet interior", A),
        ("пейзажи", "Одинокое дерево", "The lone tree", S), ("натюрморт", "Груши", "Pears", S),
        ("птицы", "Полёт", "Flight", S), ("рыбы", "Глубина", "Depth", S),
        ("натюрморт", "Олива", "Olive", S), ("абстракция", "Структура II", "Structure II", S),
    ]),
}
DEMO_CAPTION = "Демо-отметка"


class Command(BaseCommand):
    help = "Создать или удалить демонстрационные картины для проверки верстки"

    def add_arguments(self, parser):
        parser.add_argument("--remove", action="store_true")

    def handle(self, *args, **opts):
        Painting.objects.filter(sku__startswith="DEMO-").delete()
        # Отметки прежних версий команды: подпись «Демо-отметка» убираем, флаги не трогаем.
        City.objects.filter(caption_ru=DEMO_CAPTION).update(caption_ru="", caption_en="")
        if opts["remove"]:
            self.stdout.write("Демо-работы удалены.")
            return
        media = Path(settings.BASE_DIR) / "seed" / settings.SITE_THEME / "demo"
        tech = Technique.objects.first()
        for i, (cat_slug, ru, en, status, image) in enumerate(DEMO_SITES.get(settings.SITE_THEME, []), 1):
            category = Category.objects.filter(slug_ru=cat_slug).first()
            if not category:
                continue
            p = Painting(title_ru=ru, title_en=en, sku=f"DEMO-{i}", category=category, status=status,
                         technique=tech, published=True, short_ru="Демонстрационная карточка для проверки верстки.",
                         short_en="Demo card for layout checks.")
            p.full_clean()
            p.save()
            path = media / image
            if path.exists():
                with path.open("rb") as fh:
                    im = PaintingImage(painting=p, alt_ru=ru, alt_en=en)
                    im.image.save(f"demo-{i}.jpg", File(fh), save=True)
        self.stdout.write(self.style.WARNING("Созданы демо-работы (артикул DEMO-…). Удалите их: seed_demo --remove"))
