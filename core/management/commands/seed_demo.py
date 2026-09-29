"""Демонстрационные картины для локальной проверки верстки.

    python manage.py seed_demo           — создать демо-работы (артикул DEMO-…)
    python manage.py seed_demo --remove  — удалить их

Также включает демо-отметки на карте продаж (подпись «Демо-отметка»); --remove их выключает.

Не используйте на рабочем сайте: демо-работы не являются реальным ассортиментом.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from catalog.models import Category, Painting, PaintingImage, Technique
from geo.models import City

DEMO = [
    ("пейзажи", "Демо: бамбуковая тропа", "Demo: bamboo path", "available", "cover-landscape.jpg", (40, 60)),
    ("море", "Демо: тихий залив", "Demo: quiet bay", "available", "cover-sea.jpg", (60, 50)),
    ("море", "Демо: вечерний горизонт", "Demo: evening horizon", "custom", "cover-sea.jpg", None),
    ("абстракция", "Демо: раковины", "Demo: shells", "sold", "cover-abstract.jpg", (50, 50)),
    ("цветы-и-ботаника", "Демо: тюльпаны", "Demo: tulips", "custom", "cover-flowers.jpg", None),
    ("женщины", "Демо: летний образ", "Demo: summer look", "sold", "cover-women.jpg", (30, 40)),
]
DEMO_CITIES = ["Москва", "Санкт-Петербург", "Екатеринбург", "Новосибирск", "Владивосток"]
DEMO_CAPTION = "Демо-отметка"


class Command(BaseCommand):
    help = "Создать или удалить демонстрационные картины для проверки верстки"

    def add_arguments(self, parser):
        parser.add_argument("--remove", action="store_true")

    def handle(self, *args, **opts):
        Painting.objects.filter(sku__startswith="DEMO-").delete()
        City.objects.filter(caption_ru=DEMO_CAPTION).update(sale_confirmed=False, visible=False, caption_ru="", caption_en="")
        if opts["remove"]:
            self.stdout.write("Демо-работы и демо-отметки на карте удалены.")
            return
        City.objects.filter(country_code="RU", name_ru__in=DEMO_CITIES, sale_confirmed=False).update(
            sale_confirmed=True, visible=True, caption_ru=DEMO_CAPTION, caption_en="Demo mark")
        media = Path(settings.BASE_DIR) / "seed" / settings.SITE_THEME / "media"
        tech = Technique.objects.first()
        for i, (cat_slug, ru, en, status, image, size) in enumerate(DEMO, 1):
            category = Category.objects.filter(slug_ru=cat_slug).first()
            if not category:
                continue
            p = Painting(title_ru=ru, title_en=en, sku=f"DEMO-{i}", category=category, status=status,
                         technique=tech, published=True, short_ru="Демонстрационная карточка для проверки верстки.",
                         short_en="Demo card for layout checks.")
            if size:
                p.width, p.height = size
            p.full_clean()
            p.save()
            path = media / image
            if path.exists():
                with path.open("rb") as fh:
                    im = PaintingImage(painting=p, alt_ru=ru, alt_en=en)
                    im.image.save(f"demo-{i}.jpg", File(fh), save=True)
        self.stdout.write(self.style.WARNING("Созданы демо-работы (артикул DEMO-…) и демо-отметки на карте. Удалите их: seed_demo --remove"))
