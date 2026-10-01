"""Загрузить (или вернуть к стартовому виду) только страницу «Сотрудничество»; остальные страницы не затрагиваются.

    python manage.py seed_cooperation            — добавить недостающее, правки владельца сохранить
    python manage.py seed_cooperation --update   — вернуть страницу к стартовому набору (тексты, фото, пиктограммы)
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from .seed_site import Command as SeedSite


class Command(BaseCommand):
    help = "Загрузить стартовое содержимое страницы «Сотрудничество»"

    def add_arguments(self, parser):
        parser.add_argument("--update", action="store_true", help="Перезаписать страницу стартовым набором")

    def handle(self, *args, **opts):
        site = settings.SITE_THEME
        seed = SeedSite()
        seed.update = opts["update"]
        seed.media_dir = Path(settings.BASE_DIR) / "seed" / site / "media"
        seed.stdout = self.stdout
        with transaction.atomic():
            seed.cooperation(site)
        self.stdout.write(self.style.SUCCESS("Страница «Сотрудничество» загружена."))
