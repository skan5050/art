from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, FileResponse, Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.views.decorators.http import require_GET

from .i18n import ALL_LANGS, current_lang
from .labels_runtime import label
from .models import Redirect, SiteSettings
from .routing import resolve
from .seo import build_meta


def is_public(obj):
    name = obj.__class__.__name__
    if name == "Page":
        return obj.published
    if name == "Category":
        return obj.is_public()
    if name == "Painting":
        return obj.published and obj.category.is_public()
    if name == "Article":
        from content.models import Page

        guides = Page.objects.filter(kind="guides").first()
        return obj.published and guides is not None and guides.published
    if name == "CityLanding":
        from content.models import Page

        parent = Page.objects.filter(kind="cities").first()
        return obj.published and parent is not None and parent.published
    return False


def dispatch(request, path=""):
    """Единая точка входа публичных страниц: адрес → материал → общий шаблон типа."""
    full = request.path
    lang = current_lang()
    obj = resolve(full, lang)
    if obj is None:
        if not full.endswith("/"):
            if resolve(full + "/", lang) is not None or Redirect.objects.filter(old_path=full + "/").exists():
                query = request.META.get("QUERY_STRING", "")
                return HttpResponsePermanentRedirect(iri_to_uri(full + "/") + (f"?{query}" if query else ""))
        redirect = Redirect.objects.filter(old_path=full).first()
        if redirect:
            query = request.META.get("QUERY_STRING", "")
            return HttpResponsePermanentRedirect(iri_to_uri(redirect.new_path) + (f"?{query}" if query else ""))
        raise Http404

    preview = False
    if not is_public(obj):
        if not (request.user.is_authenticated and request.user.is_staff):
            raise Http404
        preview = True

    request.alternate_urls = {code: obj.url(code) for code in ALL_LANGS if obj.has_lang(code)}
    request.is_preview = preview

    name = obj.__class__.__name__
    if name == "Page":
        from content.views import page_view

        return page_view(request, obj)
    if name == "Article":
        from content.views import article_view

        return article_view(request, obj)
    if name == "CityLanding":
        from content.views import city_view

        return city_view(request, obj)
    if name == "Category":
        from catalog.views import category_view

        return category_view(request, obj)
    from catalog.views import painting_view

    return painting_view(request, obj)


def not_found(request, exception=None):
    request.alternate_urls = {}
    meta = build_meta(request, None, h1=label("error404.title"), noindex=True)
    return render(request, "pages/404.html", {"meta": meta}, status=404)


@require_GET
def robots_txt(request):
    text = SiteSettings.get().rendered_robots(request)
    return HttpResponse(text, content_type="text/plain; charset=utf-8")


@require_GET
def favicon_ico(request):
    """/favicon.ico для роботов и старых браузеров: загруженная владельцем иконка или иконка бренда темы."""
    import mimetypes

    from django.contrib.staticfiles import finders

    uploaded = SiteSettings.get().favicon
    if uploaded:
        content_type = mimetypes.guess_type(uploaded.name)[0] or "image/png"
        return FileResponse(uploaded.open("rb"), content_type=content_type)
    path = finders.find("img/favicon.ico")
    if not path:
        raise Http404
    return FileResponse(open(path, "rb"), content_type="image/x-icon")


@require_GET
def indexnow_key(request, key):
    """Файл ключа IndexNow: «адрес сайта/ключ.txt» с самим ключом внутри."""
    stored = SiteSettings.get().indexnow_key
    if not stored or key != stored:
        raise Http404
    return HttpResponse(stored, content_type="text/plain; charset=utf-8")


@require_GET
def sitemap_xml(request):
    from .sitemap import sitemap_entries

    settings = SiteSettings.get()
    entries = sitemap_entries()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for entry in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{_xml(settings.absolute(entry['path'], request))}</loc>")
        for alt_lang, alt_path in entry["alternates"]:
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{_xml(settings.absolute(alt_path, request))}"/>'
            )
        if entry.get("lastmod"):
            lines.append(f"    <lastmod>{entry['lastmod'].date().isoformat()}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    SiteSettings.objects.filter(pk=settings.pk).update(sitemap_generated_at=timezone.now())
    return HttpResponse("\n".join(lines) + "\n", content_type="application/xml; charset=utf-8")


def _xml(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


@staff_member_required
def private_file(request, path):
    """Выдача закрытых файлов (вложения заявок, импорт) только сотрудникам."""
    from django.conf import settings
    from pathlib import Path

    root = Path(settings.PRIVATE_MEDIA_ROOT).resolve()
    target = (root / path).resolve()
    if root not in target.parents or not target.is_file():
        raise Http404
    return FileResponse(open(target, "rb"), as_attachment=request.GET.get("download") == "1")


@require_GET
def geo_city(request):
    """Подсказка города для городских страниц: только страна RU и только активный лендинг; иначе пустой ответ."""
    from . import geo_detect

    payload = {}
    country, city = geo_detect.detect(request)
    if country == "RU" and city:
        landing = geo_detect.match_landing(city)
        if landing:
            payload = {"key": geo_detect.landing_key(landing), "name": landing.name_ru, "url": landing.url("ru")}
    response = JsonResponse(payload)
    response["Cache-Control"] = "private, no-store"
    response["Vary"] = "User-Agent"
    return response
