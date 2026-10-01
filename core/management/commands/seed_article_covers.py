"""Привязать обложки к статьям «Полезное» №4–20; остальное содержимое сайта не затрагивается.

    python manage.py seed_article_covers            — добавить недостающие обложки (уже загруженные не менять)
    python manage.py seed_article_covers --update   — заменить обложки и ALT стартовыми
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from .seed_site import Command as SeedSite


class Command(BaseCommand):
    help = "Загрузить обложки статей «Полезное» №4–20"

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Заменить обложки стартовыми")

    def handle(self, *args, **opts):
        site = settings.SITE_THEME
        seed = SeedSite()
        seed.update = opts["update"]
        seed.media_dir = Path(settings.BASE_DIR) / "seed" / site / "media"
        seed.stdout = self.stdout
        with transaction.atomic():
            seed.article_covers(site)
        self.stdout.write(self.style.SUCCESS("Обложки статей загружены."))
