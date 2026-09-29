"""Проверка заполненности сайта перед запуском.

    python manage.py audit_content            — отчет по текущему сайту (SITE_THEME)
    python manage.py audit_content --strict   — код выхода 1, если есть ошибки

Что проверяется:
  * парные поля RU/EN: заполнена одна версия, а вторая пуста (для опубликованных записей);
  * каждая публичная страница на обоих языках: ответ 200, один H1, Title и Description
    (длина по рекомендациям Яндекса), canonical, hreflang, alt у изображений,
    отсутствие незаполненных подстановок вида {brand} или {painting_name}.
"""
import re
from html.parser import HTMLParser

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.test import Client
from django.test.utils import override_settings

from core.i18n import LANGS
from core.routing import routable_models
from core.views import is_public

AUDIT_APPS = ("core", "catalog", "content")
SKIP_FIELDS = {"path", "slug", "canonical_override"}
PLACEHOLDER = re.compile(r"\{(brand|painting_name|category_name|seo_title|site_url|admin_path|N)\}")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.description = None
        self.canonical = None
        self.hreflang = []
        self.robots = ""
        self.images_without_alt = []
        self._skip = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self._skip += 1
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.description = a.get("content", "")
        elif tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang.append(a["hreflang"])
        elif tag == "img" and "alt" not in a:
            self.images_without_alt.append(a.get("src", ""))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.text.append(data)


def is_live(obj):
    for flag in ("published", "visible"):
        if hasattr(obj, flag) and not getattr(obj, flag):
            return False
    return True


class Command(BaseCommand):
    help = "Проверить заполненность текстов RU/EN и SEO всех публичных страниц"

    def add_arguments(self, parser):
        parser.add_argument("--strict", action="store_true", help="Завершиться с ошибкой, если найдены проблемы")

    def handle(self, *args, **opts):
        self.errors, self.warnings, self.checked = [], [], 0
        self.check_pairs()
        with override_settings(ALLOWED_HOSTS=["*"], SECURE_SSL_REDIRECT=False):
            self.check_pages()
        for w in self.warnings:
            self.stdout.write(self.style.WARNING(f"  ! {w}"))
        for e in self.errors:
            self.stdout.write(self.style.ERROR(f"  ✗ {e}"))
        summary = f"Проверено страниц: {self.checked}. Ошибок: {len(self.errors)}, предупреждений: {len(self.warnings)}"
        if self.errors and opts["strict"]:
            raise CommandError(summary)
        self.stdout.write((self.style.SUCCESS if not self.errors else self.style.WARNING)(summary))

    # --- парные поля ---
    def check_pairs(self):
        for model in apps.get_models():
            if model._meta.app_label not in AUDIT_APPS:
                continue
            names = {f.name for f in model._meta.get_fields() if isinstance(f, (models.CharField, models.TextField))}
            pairs = sorted(n[:-3] for n in names if n.endswith("_ru") and f"{n[:-3]}_en" in names and n[:-3] not in SKIP_FIELDS)
            if not pairs:
                continue
            for obj in model.objects.all():
                if not is_live(obj):
                    continue
                for base in pairs:
                    ru, en = getattr(obj, f"{base}_ru") or "", getattr(obj, f"{base}_en") or ""
                    if bool(ru.strip()) != bool(en.strip()):
                        missing = "EN" if ru.strip() else "RU"
                        self.errors.append(f"{model._meta.verbose_name} «{obj}»: поле «{base}» — нет версии {missing}")

    # --- страницы ---
    def check_pages(self):
        client = Client()
        for model in routable_models():
            for obj in model.objects.all():
                if not is_public(obj):
                    continue
                for lang in LANGS:
                    if obj.has_lang(lang):
                        self.check_url(client, obj.url(lang), lang)

    def check_url(self, client, url, lang):
        self.checked += 1
        r = client.get(url, follow=False)
        if r.status_code != 200:
            self.errors.append(f"{url}: ответ {r.status_code}")
            return
        p = PageParser()
        p.feed(r.content.decode("utf-8"))
        title = p.title.strip()
        if p.h1 != 1:
            self.errors.append(f"{url}: H1 на странице — {p.h1} (нужен ровно один)")
        if not title:
            self.errors.append(f"{url}: пустой Title")
        elif len(title) > 75:
            self.warnings.append(f"{url}: Title длиннее 75 символов ({len(title)})")
        if not p.description:
            self.errors.append(f"{url}: нет meta description")
        elif not 50 <= len(p.description) <= 200:
            self.warnings.append(f"{url}: Description {len(p.description)} символов (рекомендуется 50–200)")
        if not p.canonical:
            self.errors.append(f"{url}: нет canonical")
        if len(LANGS) > 1 and "noindex" not in p.robots and p.hreflang and "x-default" not in p.hreflang:
            self.errors.append(f"{url}: hreflang без x-default")
        for src in p.images_without_alt:
            self.errors.append(f"{url}: изображение без alt ({src})")
        text = " ".join(p.text) + " " + title + " " + (p.description or "")
        for m in set(PLACEHOLDER.findall(text)):
            self.errors.append(f"{url}: незаполненная подстановка {{{m}}}")
