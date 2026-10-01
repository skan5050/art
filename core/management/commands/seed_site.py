"""Первичное наполнение установки сайта стартовыми материалами.

    python manage.py seed_site            — данные для темы из SITE_THEME (a или d)
    python manage.py seed_site --update   — перезаписать тексты стартовыми (осторожно)

Команда повторяемая: существующие записи без --update не меняются,
поэтому правки, сделанные в админке, сохраняются.
"""
import datetime
import importlib
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Category, Technique
from content.models import (Article, CityLanding, CooperationAdvantage, CooperationBlock, CooperationContent, HomeSection, MenuItem, Page,
                            Review, StudioImage)
from geo.models import City
from core.labels import DEFAULT_LABELS
from core.models import Label, SeoTemplate, SharedBlock, SiteSettings, StandardSize, Translation

SIZES = [
    ("rect", [(20, 30), (30, 40), (40, 50), (40, 60), (50, 60), (50, 70), (60, 80), (60, 90), (70, 100), (80, 100), (80, 120)]),
    ("square", [(30, 30), (40, 40), (50, 50), (60, 60), (80, 80), (100, 100)]),
    ("pano", [(30, 60), (40, 80), (50, 100)]),
]


class Command(BaseCommand):
    help = "Загрузить стартовые тексты, рубрики, SEO и настройки сайта"

    def add_arguments(self, parser):
        parser.add_argument("--site", choices=["a", "d"], default=None, help="По умолчанию — SITE_THEME")
        parser.add_argument("--update", action="store_true", help="Перезаписать существующие тексты стартовыми")

    def handle(self, *args, **opts):
        site = opts["site"] or settings.SITE_THEME
        self.update = opts["update"]
        self.media_dir = Path(settings.BASE_DIR) / "seed" / site / "media"
        data = importlib.import_module(f"seed.{site}.data")
        articles = importlib.import_module(f"seed.{site}.articles")
        with transaction.atomic():
            self.settings(data.SETTINGS)
            self.labels(getattr(data, "LABELS", {}))
            self.blocks(data.BLOCKS)
            self.sizes()
            self.seo_templates(data.SEO_TEMPLATES)
            self.techniques(data.TECHNIQUES)
            pages = self.pages(data.PAGES)
            self.categories(data.CATEGORIES)
            self.menu(data.MENU, pages)
            self.cooperation(site)
            self.home_sections(data.HOME_SECTIONS)
            self.articles(articles.ARTICLES)
            self.studio(getattr(data, "STUDIO_IMAGES", []))
            self.city_pages(site)
            self.reviews(site)
            self.chinese(site)
        self.stdout.write(self.style.SUCCESS(f"Наполнение сайта «{data.SETTINGS['brand_name_ru']}» загружено."))

    # --- помощники ---
    def attach(self, obj, field, filename):
        if not filename:
            return
        current = getattr(obj, field)
        if current and not self.update:
            return
        path = self.media_dir / filename
        if path.exists():
            if current:
                current.delete(save=False)  # прежний файл убираем, чтобы у нового не появлялся случайный суффикс в имени
            with path.open("rb") as fh:
                getattr(obj, field).save(filename, File(fh), save=False)

    def upsert(self, model, lookup, values, files=None):
        obj = model.objects.filter(**lookup).first()
        created = obj is None
        if created:
            obj = model(**lookup)
        if created or self.update:
            for key, value in values.items():
                setattr(obj, key, value)
        for field, filename in (files or {}).items():
            self.attach(obj, field, filename)
        if created or self.update or files:
            obj.save()
        return obj

    # --- разделы ---
    def settings(self, values):
        values = dict(values)
        files = {k: values.pop(k) for k in ("logo", "logo_on_dark", "favicon", "certificate_image") if k in values}
        obj = SiteSettings.get()
        fresh = not obj.logo and obj.brand_name_en == ""
        if fresh or self.update:
            for key, value in values.items():
                setattr(obj, key, value)
        for field, filename in files.items():
            self.attach(obj, field, filename)
        obj.save()

    def labels(self, overrides):
        for key, (group, ru, en, hint) in DEFAULT_LABELS.items():
            ru, en = overrides.get(key, (ru, en))
            self.upsert(Label, {"key": key}, {"group": group, "hint": hint, "value_ru": ru, "value_en": en})

    def blocks(self, blocks):
        for item in blocks:
            item = dict(item)
            key = item.pop("key")
            self.upsert(SharedBlock, {"key": key}, item)

    def sizes(self):
        if StandardSize.objects.exists() and not self.update:
            return
        order = 0
        for group, items in SIZES:
            for w, h in items:
                order += 10
                StandardSize.objects.update_or_create(width=w, height=h, defaults={"group": group, "order": order, "visible": True})

    def seo_templates(self, templates):
        for kind, values in templates.items():
            self.upsert(SeoTemplate, {"kind": kind}, values)

    def techniques(self, items):
        for i, (ru, en) in enumerate(items):
            self.upsert(Technique, {"name_ru": ru}, {"name_en": en, "order": i * 10})

    def pages(self, pages):
        result = {}
        for i, item in enumerate(pages):
            item = dict(item)
            kind = item.pop("kind")
            files = {k: item.pop(k) for k in ("image", "banner_image", "banner_image_mobile", "og_image") if k in item}
            item.setdefault("order", i * 10)
            lookup = {"kind": kind} if kind != "text" else {"kind": kind, "slug_ru": item["slug_ru"]}
            result[kind if kind != "text" else item["slug_ru"]] = self.upsert(Page, lookup, item, files)
        return result

    def categories(self, items, parent=None):
        for i, item in enumerate(items):
            item = dict(item)
            children = item.pop("children", [])
            files = {"cover": item.pop("cover")} if item.get("cover") else {}
            item.pop("cover", None)
            item.setdefault("order", i * 10)
            item["parent"] = parent
            obj = self.upsert(Category, {"parent": parent, "slug_ru": item["slug_ru"]}, item, files)
            if self.update and not files and obj.cover:
                obj.cover.delete(save=False)  # обложки нет в наполнении — остаётся штатная заглушка макета
                obj.cover = None
                obj.save()
            self.categories(children, obj)

    def menu(self, items, pages):
        if MenuItem.objects.exists() and not self.update:
            return
        MenuItem.objects.all().delete()
        for i, spec in enumerate(items):
            if isinstance(spec, dict):
                spec = dict(spec)
                kind = spec.pop("page")
            else:
                kind, visible = spec if isinstance(spec, tuple) else (spec, True)
                spec = {"visible": visible}
            page = pages.get(kind)
            if page:
                MenuItem.objects.create(page=page, order=i * 10, **spec)

    def cooperation(self, site):
        """Страница «Сотрудничество»: страница, пункт меню, содержимое, блоки, преимущества и китайские тексты.

        Без --update существующее содержимое (правки владельца) не меняется; недостающее добавляется.
        """
        spec = importlib.import_module("seed.cooperation")
        page_spec = dict(spec.PAGE[site])
        zh_page = page_spec.pop("zh")
        existed = Page.objects.filter(kind="cooperation").exists()
        page = self.upsert(Page, {"kind": "cooperation"}, {**page_spec, "order": 45})
        if (not existed or self.update) and not MenuItem.objects.filter(page=page).exists():
            MenuItem.objects.create(page=page, order=45, visible=True)
        self.put_zh_fields(page, zh_page)

        data = spec.CONTENT[site]
        content = CooperationContent.objects.order_by("pk").first()
        created = content is None
        if created:
            content = CooperationContent()
        if created or self.update:
            for key, value in data["scalars"].items():
                setattr(content, key, value)
        for field, filename in data["images"].items():
            self.attach(content, field, filename)
        content.save()
        self.put_zh_fields(content, data["zh"])

        for i, item in enumerate(data["blocks"]):
            block = content.blocks.filter(order=i * 10).first()
            fresh = block is None
            if fresh:
                block = CooperationBlock(content=content, order=i * 10)
            if fresh or self.update:
                for key in ("title_ru", "title_en", "text_ru", "text_en", "alt_ru", "alt_en"):
                    setattr(block, key, item[key])
                block.image_side = item["side"]
            self.attach(block, "image", item["image"])
            block.save()
            self.put_zh_fields(block, item["zh"])
        for i, item in enumerate(data["advantages"]):
            adv = content.advantages.filter(order=i * 10).first()
            fresh = adv is None
            if fresh:
                adv = CooperationAdvantage(content=content, order=i * 10)
            if fresh or self.update:
                adv.icon_key = item["icon"]
                for key in ("title_ru", "title_en", "text_ru", "text_en"):
                    setattr(adv, key, item[key])
                adv.save()
            self.put_zh_fields(adv, item["zh"])

    def home_sections(self, sections):
        for i, item in enumerate(sections):
            item = dict(item)
            kind = item.pop("kind")
            files = {"image": item.pop("image")} if item.get("image") else {}
            item.pop("image", None)
            item.setdefault("order", i * 10)
            self.upsert(HomeSection, {"kind": kind}, item, files)

    def articles(self, items):
        for i, item in enumerate(items):
            item = dict(item)
            categories = item.pop("categories", [])
            files = {"cover": item.pop("cover")} if item.get("cover") else {}
            item.pop("cover", None)
            item.setdefault("order", i * 10)
            item.setdefault("published", i < 3)  # для согласования открыты три статьи; остальные — черновики
            obj = self.upsert(Article, {"slug_ru": item["slug_ru"]}, item, files)
            if categories:
                obj.related_categories.set(Category.objects.filter(slug_ru__in=categories))

    def studio(self, items):
        if StudioImage.objects.exists() and not self.update:
            return
        if self.update:
            StudioImage.objects.all().delete()
        for i, item in enumerate(items):
            item = dict(item)
            filename = item.pop("image")
            obj = StudioImage(order=i * 10, **item)
            self.attach(obj, "image", filename)
            if obj.image:
                obj.save()

    def reviews(self, site):
        """Стартовые отзывы из комплекта заказчика; отзывы, добавленные в админке, не затрагиваются."""
        try:
            data = importlib.import_module(f"seed.{site}.reviews")
        except ImportError:
            return
        for i, item in enumerate(data.REVIEWS):
            item = dict(item)
            photo = item.pop("photo", "")
            item.pop("painting_note", None)
            if item.get("date"):
                item["date"] = datetime.date.fromisoformat(item["date"])
            lookup = {"author_ru": item.pop("author_ru"), "city_ru": item.pop("city_ru")}
            item.update({"published": True, "order": i * 10, "featured": item.get("featured", False)})
            self.upsert(Review, lookup, item, {"photo": photo})

    def put_zh(self, target, field, text):
        """Один китайский перевод: существующие правки владельца без --update не перезаписываются."""
        if not text:
            return
        row = Translation.objects.filter(lang="zh", target=target, field=field).first()
        if row is None:
            Translation.objects.create(lang="zh", target=target, field=field, text=text)
        elif self.update and row.text != text:
            row.text = text
            row.save(update_fields=["text"])

    def put_zh_fields(self, obj, fields):
        if obj is None:
            return
        target = f"{obj._meta.label_lower}:{obj.pk}"
        for field, text in fields.items():
            self.put_zh(target, field, text)

    def chinese(self, site):
        """Китайская версия (/zh/): переводы надписей, страниц, рубрик, статей, городов и отзывов."""
        from catalog.models import Painting
        from content.models import Review

        try:
            data = importlib.import_module(f"seed.{site}.zh")
        except ImportError:
            return
        common = importlib.import_module("seed.zh_common")
        for key, text in {**common.LABELS, **getattr(data, "LABELS", {})}.items():
            self.put_zh(f"label:{key}", "value", text)
        self.put_zh_fields(SiteSettings.get(), getattr(data, "SETTINGS", {}))
        for key, fields in getattr(data, "BLOCKS", {}).items():
            self.put_zh_fields(SharedBlock.objects.filter(key=key).first(), fields)
        for kind, fields in getattr(data, "SEO_TEMPLATES", {}).items():
            self.put_zh_fields(SeoTemplate.objects.filter(kind=kind).first(), fields)
        for name, text in getattr(data, "TECHNIQUES", {}).items():
            self.put_zh_fields(Technique.objects.filter(name_ru=name).first(), {"name": text})
        for kind, fields in getattr(data, "PAGES", {}).items():
            self.put_zh_fields(Page.objects.filter(kind=kind).first(), fields)
        for kind, fields in getattr(data, "HOME_SECTIONS", {}).items():
            self.put_zh_fields(HomeSection.objects.filter(kind=kind).first(), fields)
        for item in MenuItem.objects.select_related("page"):
            key = item.label_ru or (item.page.kind if item.page else item.url)
            text = getattr(data, "MENU", {}).get(key)
            if text:
                self.put_zh_fields(item, {"label": text})
        for path, fields in getattr(data, "CATEGORIES", {}).items():
            self.put_zh_fields(Category.objects.filter(path_ru=path).first(), fields)
        for slug, fields in getattr(data, "ARTICLES", {}).items():
            self.put_zh_fields(Article.objects.filter(slug_ru=slug).first(), fields)
        cities = {**common.typical_landings(site), **getattr(data, "CITY_LANDINGS", {})}
        for name, fields in cities.items():
            self.put_zh_fields(CityLanding.objects.filter(name_ru=name).first(), fields)
        for key, fields in getattr(data, "REVIEWS", {}).items():
            author, _, city = key.partition("|")
            self.put_zh_fields(Review.objects.filter(author_ru=author, city_ru=city).first(), fields)
        for sku, fields in getattr(data, "PAINTINGS", {}).items():
            self.put_zh_fields(Painting.objects.filter(sku=sku).first(), fields)
        for position, fields in getattr(data, "STUDIO", {}).items():
            self.put_zh_fields(StudioImage.objects.filter(alt_ru=position).first(), fields)
        for source_id, (name, country) in common.CITY_NAMES.items():
            self.put_zh_fields(City.objects.filter(source="GeoNames", source_id=source_id).first(), {"name": name, "country": country})

    def city_pages(self, site):
        """Городские страницы: у каждой свой текст; адрес и координаты владелец вносит сам."""
        try:
            data = importlib.import_module(f"seed.{site}.cities")
        except ImportError:
            return
        page = dict(data.PAGE)
        kind = page.pop("kind")
        page.setdefault("order", 95)
        self.upsert(Page, {"kind": kind}, page)
        for i, item in enumerate(data.CITIES):
            item = dict(item)
            source_id, to = item.pop("source_id"), item.pop("to")
            item["delivery_ru"] = data.DELIVERY_RU.format(to=to)
            item["delivery_en"] = data.DELIVERY_EN.format(name=item["name_en"])
            item.setdefault("seo_description_en", f"Paintings in stock and made to order with delivery to {item['name_en']}. "
                                                   "Delivery via CDEK or another carrier by agreement; paid separately.")
            item["city"] = City.objects.filter(source="GeoNames", source_id=source_id).first()
            item.setdefault("order", i * 10)
            item.setdefault("published", True)
            self.upsert(CityLanding, {"name_ru": item["name_ru"]}, item)

