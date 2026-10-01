from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import select_template

from catalog.models import Category, Painting
from catalog.views import paginate_paintings
from core.i18n import current_lang, tr
from core.labels_runtime import label
from core.seo import article_jsonld, build_meta, organization_jsonld
from core.sitemap import is_empty_listing
from geo.major_cities import PRIORITY
from geo.models import City

from .models import Article, CertificateNominal, CityLanding, HomeSection, Page, Review, StudioImage


def crumbs_for_page(page):
    lang = current_lang()
    home = Page.objects.filter(kind="home").first()
    items = []
    if home and page.kind != "home":
        items.append({"label": label("nav.home"), "href": home.url(lang)})
    items.append({"label": page.nav_title, "href": page.url(lang)})
    return items


def _public_categories(parent=None):
    lang = current_lang()
    qs = Category.objects.filter(parent=parent, visible=True)
    return [c for c in qs if c.url(lang)]


def _home_sections():
    lang = current_lang()
    sections = []
    for section in HomeSection.objects.filter(visible=True).prefetch_related("paintings"):
        data = {"obj": section, "kind": section.kind}
        if section.kind in ("available", "custom", "sold"):
            chosen = [p for p in section.paintings.all() if p.published and p.url(lang)]
            if not chosen:
                status = {"available": Painting.AVAILABLE, "custom": Painting.CUSTOM, "sold": Painting.SOLD}[section.kind]
                chosen = [p for p in Painting.objects.filter(published=True, status=status).prefetch_related("images")[: section.limit * 2] if p.url(lang)]
            data["paintings"] = chosen[: section.limit]
            if not data["paintings"]:
                continue
        elif section.kind == "categories":
            data["categories"] = _public_categories()[: section.limit or None]
        elif section.kind == "reviews":
            data["reviews"] = [r for r in Review.objects.filter(published=True)[: section.limit] if tr(r, "text")]
            if not data["reviews"]:
                continue
        elif section.kind == "guides":
            data["articles"] = [a for a in Article.objects.filter(published=True)[: section.limit] if a.url(lang)]
            if not data["articles"]:
                continue
        sections.append(data)
    return sections


def page_view(request, page):
    lang = current_lang()
    context = {"page": page, "crumbs": crumbs_for_page(page)}
    jsonld, page_num = [], 1
    og_image = page.banner_image.url if page.banner_image else (page.image.url if page.image else "")

    if page.kind == "home":
        context["sections"] = _home_sections()
        context["crumbs"] = []
        jsonld = organization_jsonld(request)
    elif page.kind == "catalog":
        context["categories"] = _public_categories()
    elif page.kind == "sold":
        context["cities"] = _map_cities(lang)
        qs = Painting.objects.filter(published=True, status=Painting.SOLD)
        paged = paginate_paintings(request, qs, page)
        if not isinstance(paged, dict):
            return paged
        context.update(paged)
        page_num = paged["page_obj"].number
    elif page.kind == "reviews":
        context["reviews"] = [r for r in Review.objects.filter(published=True) if tr(r, "text")]
    elif page.kind == "delivery":
        context["cities"] = _map_cities(lang)
        context["geo_attribution"] = 'Города: <a href="https://www.geonames.org/">GeoNames</a> (CC BY 4.0)'

    elif page.kind == "contacts":
        context.update(_inline_form_context(request))
    elif page.kind == "certificate":
        context["nominals"] = list(CertificateNominal.objects.filter(visible=True))
    elif page.kind == "guides":
        context["articles"] = [a for a in Article.objects.filter(published=True) if a.url(lang)]
    elif page.kind == "cities":
        context["landings"] = [c for c in CityLanding.objects.filter(published=True) if c.url(lang)]
    elif page.kind in ("about", "studio"):
        context["studio_images"] = list(StudioImage.objects.filter(visible=True))
        studio = Page.objects.filter(kind="studio", published=True).first()
        context["studio_page"] = studio if studio and studio.url(lang) and page.kind == "about" else None

    if request.headers.get("x-requested-with") == "fetch" and "paintings" in context:
        from catalog.views import fragment_response

        return fragment_response(request, context)

    meta = build_meta(
        request, page, h1=page.t.title, fallback_description=page.t.intro or page.t.body,
        page_num=page_num, noindex=is_empty_listing(page) or getattr(request, "is_preview", False),
        og_image_url=og_image, breadcrumbs=context["crumbs"] if len(context["crumbs"]) > 1 else None,
        jsonld_extra=jsonld,
    )
    context["meta"] = meta
    try:
        template = select_template([f"pages/{page.kind}.html", "pages/text.html"])
    except TemplateDoesNotExist:
        raise
    return render(request, template.template.name, context)


def _map_cities(lang):
    landing_urls = _landing_urls(lang)
    cities = []
    for city in City.objects.filter(sale_confirmed=True, visible=True):
        cities.append({
            "name": (city.name_en or city.name_source) if lang == "en" else (tr(city, "name", "zh") or city.name_en or city.name_source) if lang == "zh" else city.name_ru,
            "country": (city.country_en or city.country_code) if lang == "en" else (tr(city, "country", "zh") or city.country_en or city.country_code) if lang == "zh" else city.country_ru,
            "lat": float(city.latitude),
            "lng": float(city.longitude),
            "caption": tr(city, "caption", lang),
            "code": city.country_code,
            "landing": landing_urls.get(city.pk, ""),
            "rank": PRIORITY.get(city.source_id, 1000 - min(city.population or 0, 10**8) / 10**5),
        })
    cities.sort(key=lambda c: (c["code"] != "RU", c["country"], c["rank"]))
    return cities


def _landing_urls(lang):
    """Ссылки на опубликованные городские страницы для подсказок карты (город → URL)."""
    try:
        from content.models import CityLanding
    except ImportError:
        return {}
    return {l.city_id: l.url(lang) for l in CityLanding.objects.filter(published=True, city__isnull=False) if l.url(lang)}


def article_view(request, article):
    lang = current_lang()
    guides = Page.objects.filter(kind="guides").first()
    crumbs = crumbs_for_page(guides) if guides else []
    crumbs.append({"label": article.t.title, "href": article.url(lang)})
    related = [a for a in Article.objects.filter(published=True).exclude(pk=article.pk)[:3] if a.url(lang)]
    context = {
        "article": article,
        "guides": guides,
        "crumbs": crumbs,
        "related_articles": related,
        "related_categories": [c for c in article.related_categories.filter(visible=True) if c.url(lang)],
        "related_paintings": [p for p in article.related_paintings.filter(published=True) if p.url(lang)],
    }
    context["meta"] = build_meta(
        request, article, h1=article.t.title, fallback_description=article.t.excerpt or article.t.body,
        og_image_url=article.cover.url if article.cover else "", og_type="article", breadcrumbs=crumbs,
        noindex=getattr(request, "is_preview", False), jsonld_extra=[article_jsonld(request, article)],
    )
    return render(request, "pages/article.html", context)


def city_view(request, landing):
    """Городская страница: свой текст, работы, отзывы из города, адрес с картой, доставка и заявка."""
    lang = current_lang()
    parent = Page.objects.filter(kind="cities").first()
    crumbs = crumbs_for_page(parent) if parent else []
    crumbs.append({"label": landing.t.name, "href": landing.url(lang)})
    works = [p for p in Painting.objects.filter(published=True).exclude(status=Painting.SOLD)
             .select_related("category").order_by("-id")[:8] if p.url(lang)]
    reviews = [r for r in Review.objects.filter(published=True, city_ru__iexact=landing.name_ru) if tr(r, "text")]
    others = [c for c in CityLanding.objects.filter(published=True).exclude(pk=landing.pk) if c.url(lang)]
    context = {
        "landing": landing,
        "cities_page": parent,
        "crumbs": crumbs,
        "works": works,
        "city_reviews": reviews,
        "other_landings": others,
    }
    if lang == "ru":  # автоопределение города — только для русских городских страниц (ТЗ), только как предложение
        from core import geo_detect
        from django.urls import reverse

        picker = geo_detect.picker_items()
        context["city_geo"] = {
            "endpoint": reverse("geo-city"), "days": 30,
            "current": {"key": geo_detect.landing_key(landing), "name": landing.name_ru, "url": landing.url("ru")},
            "cities": picker,
            "labels": {
                "region": "Ваш город", "ask": "Ваш город — {city}?", "yes": "Да, верно", "yes_short": "Да", "other": "Выбрать другой",
                "other_short": "Другой город", "go": "Перейти: {city}", "stay": "Остаться: {city}", "close": "Закрыть",
                "search": "Поиск города",
            },
        }
    context["meta"] = build_meta(
        request, landing, h1=landing.t.title, fallback_description=landing.t.intro or landing.t.body,
        og_image_url=landing.cover.url if landing.cover else "", breadcrumbs=crumbs,
        noindex=getattr(request, "is_preview", False),
    )
    return render(request, "pages/city.html", context)


def _inline_form_context(request):
    """Контекст встроенной формы на странице контактов (работает и без JavaScript)."""
    from catalog.views import common_sizes

    kind = request.GET.get("order", "question")
    painting = category = None
    if request.GET.get("painting", "").isdigit():
        painting = Painting.objects.filter(pk=int(request.GET["painting"]), published=True).first()
    if request.GET.get("category", "").isdigit():
        category = Category.objects.filter(pk=int(request.GET["category"]), visible=True).first()
    if painting:
        kind = "similar" if painting.is_sold else "painting"
    elif category:
        kind = "category"
    elif kind not in ("general", "custom", "delivery", "question", "certificate"):
        kind = "question"
    title_key = {"painting": "form.title.painting", "similar": "form.title.similar", "category": "form.title.category",
                 "delivery": "form.title.delivery", "certificate": "form.title.certificate"}.get(kind, "form.title.general")
    sizes = painting.desired_sizes() if painting and painting.status != Painting.AVAILABLE else common_sizes()
    return {
        "inline_kind": kind,
        "inline_painting": painting,
        "inline_category": category,
        "inline_sizes": sizes,
        "inline_title": label(title_key),
    }
