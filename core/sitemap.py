"""Состав sitemap.xml: только опубликованные, индексируемые, канонические страницы."""
from .i18n import LANGS
from .routing import routable_models


def is_empty_listing(obj):
    """Пустые списки (отзывы, SOLD, рубрики без работ) — noindex и вне sitemap (приложение Д2)."""
    name = obj.__class__.__name__
    if name == "Category":
        return not obj.has_content()
    if name == "Page":
        if obj.kind == "reviews":
            from content.models import Review

            return not Review.objects.filter(published=True).exists()
        if obj.kind == "sold":
            from catalog.models import Painting

            return not Painting.objects.filter(published=True, status=Painting.SOLD).exists()
        if obj.kind == "guides":
            from content.models import Article

            return not Article.objects.filter(published=True).exists()
    return False


def sitemap_entries():
    from .views import is_public

    entries = []
    for model in routable_models():
        for obj in model.objects.all():
            if not getattr(obj, "indexable", True) or not is_public(obj) or is_empty_listing(obj):
                continue
            langs = [code for code in LANGS if obj.has_lang(code)]
            alternates = [(code, obj.url(code)) for code in langs] if len(langs) > 1 else []
            if alternates:
                alternates.append(("x-default", obj.url("ru")))
            for code in langs:
                entries.append({
                    "path": obj.url(code),
                    "alternates": alternates,
                    "lastmod": getattr(obj, "updated_at", None),
                })
    entries.sort(key=lambda e: (e["path"].startswith("/en/"), len(e["path"]), e["path"]))
    return entries
