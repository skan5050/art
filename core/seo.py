"""Метаданные страниц: Title, description, canonical, hreflang, Open Graph, JSON-LD.

Правило Title: «{brand} | {seo_title}» (раздел 11.3 ТЗ). В записи хранится только
смысловая часть; бренд подставляется из «Общие настройки → Бренд».
Микроразметка строится только из фактически заполненных данных.
"""
import json
import re

from django.utils.safestring import mark_safe

from .i18n import LANGS, current_lang, tr
from .models import SeoTemplate, SiteSettings
from .text import plain_text

_VAR = re.compile(r"\{(\w+)\}")


def fill_template(template, variables):
    """Подстановка переменных. Если нужного значения нет — шаблон не применяется."""
    if not template:
        return ""
    missing = [name for name in _VAR.findall(template) if not variables.get(name)]
    if missing:
        return ""
    return _VAR.sub(lambda m: str(variables[m.group(1)]), template)


def _template(kind, field, lang):
    tpl = SeoTemplate.objects.filter(kind=kind).first()
    return tr(tpl, field, lang) if tpl else ""


def object_variables(obj, lang, brand):
    variables = {"brand": brand}
    title = tr(obj, "title", lang) or tr(obj, "name", lang)
    if obj.__class__.__name__ == "Painting":
        variables["painting_name"] = title
    if obj.__class__.__name__ == "Category":
        variables["category_name"] = title
    variables["title"] = title
    return variables


def build_meta(request, obj=None, *, h1="", fallback_description="", page_num=1, noindex=False,
               og_image_url="", og_type="website", breadcrumbs=None, jsonld_extra=None):
    settings = SiteSettings.get()
    lang = current_lang()
    brand = settings.brand(lang)

    seo_title, description = "", ""
    if obj is not None:
        variables = object_variables(obj, lang, brand)
        kind = obj.seo_kind()
        seo_title = tr(obj, "seo_title", lang) or fill_template(_template(kind, "title", lang), variables)
        description = tr(obj, "seo_description", lang) or fill_template(_template(kind, "description", lang), variables)
        seo_title = seo_title or h1 or variables["title"]
    seo_title = (seo_title or h1).replace("{brand}", brand)
    description = plain_text(description or fallback_description, brand, limit=300)

    if page_num > 1:
        list_tpl = _template("list_page", "title", lang) or "{seo_title} — страница {N}"
        seo_title = list_tpl.replace("{seo_title}", seo_title).replace("{N}", str(page_num))
        from .labels_runtime import label

        if description:
            description = f"{description.rstrip('.')}. {label('catalog.page', lang)} {page_num}."

    title = f"{brand} | {seo_title}" if seo_title and seo_title != brand else brand

    canonical, alternates = "", []
    if obj is not None:
        suffix = f"?page={page_num}" if page_num > 1 else ""
        override = (getattr(obj, "canonical_override", "") or "").strip()
        if override.startswith("http"):
            canonical = override
        elif override.startswith("/"):
            canonical = settings.absolute(override, request)
        else:
            canonical = settings.absolute(obj.url(lang) + suffix, request)
        present = [code for code in LANGS if obj.has_lang(code)]
        if len(present) > 1:
            for code in present:
                alternates.append({"lang": code, "href": settings.absolute(obj.url(code) + suffix, request)})
            alternates.append({"lang": "x-default", "href": settings.absolute(obj.url("ru") + suffix, request)})

    indexable = not noindex and (obj is None or getattr(obj, "indexable", True))

    og_title = (tr(obj, "og_title", lang) if obj is not None else "") or seo_title or brand
    og_description = (tr(obj, "og_description", lang) if obj is not None else "") or description
    image = ""
    if obj is not None and getattr(obj, "og_image", None):
        image = obj.og_image.url
    image = image or og_image_url or (settings.logo.url if settings.logo else "")
    if image and image.startswith("/"):
        image = settings.absolute(image, request)

    jsonld = []
    if breadcrumbs:
        jsonld.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": crumb["label"],
                 "item": settings.absolute(crumb["href"], request)}
                for i, crumb in enumerate(breadcrumbs) if crumb.get("href")
            ],
        })
    if jsonld_extra:
        jsonld.extend(jsonld_extra)

    return {
        "title": title,
        "description": description,
        "canonical": canonical,
        "alternates": alternates,
        "robots": "index, follow" if indexable else "noindex, follow",
        "indexable": indexable,
        "og": {"title": og_title, "description": og_description, "image": image, "url": canonical, "type": og_type},
        "jsonld": [mark_safe(json.dumps(item, ensure_ascii=False).replace("</", "<\\/")) for item in jsonld],
    }


def organization_jsonld(request):
    settings = SiteSettings.get()
    lang = current_lang()
    home = settings.absolute("/en/" if lang == "en" else "/", request)
    org = {"@context": "https://schema.org", "@type": "Organization", "name": settings.brand(lang), "url": home}
    if settings.logo:
        org["logo"] = settings.absolute(settings.logo.url, request)
    contact = {}
    if settings.phone:
        contact["telephone"] = settings.phone
    if settings.email:
        contact["email"] = settings.email
    if contact:
        org["contactPoint"] = {"@type": "ContactPoint", "contactType": "customer service", **contact}
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": settings.brand(lang), "url": home,
               "inLanguage": lang}
    return [website, org]


def article_jsonld(request, article):
    settings = SiteSettings.get()
    lang = current_lang()
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": tr(article, "title", lang)[:110],
        "inLanguage": lang,
        "mainEntityOfPage": settings.absolute(article.url(lang), request),
        "datePublished": article.published_at.isoformat(),
        "dateModified": article.updated_at.isoformat(),
        "publisher": {"@type": "Organization", "name": settings.brand(lang)},
        "author": {"@type": "Organization", "name": settings.brand(lang)},
    }
    if article.cover:
        data["image"] = settings.absolute(article.cover.url, request)
    return data
