from django.core.paginator import Paginator
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri

from core.i18n import current_lang
from core.labels_runtime import label
from core.models import SiteSettings, StandardSize
from core.seo import build_meta
from core.sitemap import is_empty_listing

from .models import Category, Painting, size_option


def paginate_paintings(request, queryset, owner):
    """Постраничный список: ?page=N с собственным URL и canonical (раздел 12.3)."""
    lang = current_lang()
    raw = request.GET.get("page")
    number = 1
    if raw is not None:
        if not raw.isdigit() or int(raw) < 1:
            raise Http404
        number = int(raw)
        if number == 1:
            return HttpResponsePermanentRedirect(iri_to_uri(owner.url(lang)))
    per_page = SiteSettings.get().per_page
    queryset = queryset.select_related("category", "technique").prefetch_related("images")
    items = [p for p in queryset if p.url(lang)]
    paginator = Paginator(items, per_page)
    if number > max(paginator.num_pages, 1):
        raise Http404
    page_obj = paginator.page(number)
    base = owner.url(lang)
    return {
        "paintings": list(page_obj.object_list),
        "page_obj": page_obj,
        "paginator": paginator,
        "page_links": [{"number": n, "href": base if n == 1 else f"{base}?page={n}"} for n in paginator.page_range],
        "prev_url": (base if page_obj.number == 2 else f"{base}?page={page_obj.number - 1}") if page_obj.has_previous() else "",
        "next_url": f"{base}?page={page_obj.number + 1}" if page_obj.has_next() else "",
    }


def fragment_response(request, context):
    """Ответ для кнопки «Показать еще»: карточки следующей страницы и адрес следующей."""
    html = render_to_string("catalog/_cards.html", context, request=request)
    return JsonResponse({"html": html, "next": context.get("next_url", "")})


def category_crumbs(category):
    from content.models import Page

    lang = current_lang()
    crumbs = []
    home = Page.objects.filter(kind="home").first()
    catalog = Page.objects.filter(kind="catalog").first()
    if home:
        crumbs.append({"label": label("nav.home"), "href": home.url(lang)})
    if catalog:
        crumbs.append({"label": catalog.nav_title, "href": catalog.url(lang)})
    for node in category.ancestors(include_self=True):
        crumbs.append({"label": node.t.name, "href": node.url(lang)})
    return crumbs


def category_view(request, category):
    lang = current_lang()
    subcategories = [c for c in category.children.filter(visible=True) if c.url(lang)]
    paged = paginate_paintings(request, category.public_paintings(), category)
    if not isinstance(paged, dict):
        return paged
    context = {"category": category, "subcategories": subcategories, "crumbs": category_crumbs(category), **paged}
    if request.headers.get("x-requested-with") == "fetch":
        return fragment_response(request, context)
    context["parent"] = category.parent
    context["meta"] = build_meta(
        request, category, h1=category.t.name, fallback_description=category.t.intro,
        page_num=paged["page_obj"].number, breadcrumbs=context["crumbs"],
        noindex=is_empty_listing(category) or getattr(request, "is_preview", False),
        og_image_url=category.cover.url if category.cover else "",
    )
    return render(request, "catalog/category.html", context)


def painting_view(request, painting):
    lang = current_lang()
    crumbs = category_crumbs(painting.category) + [{"label": painting.t.title, "href": painting.url(lang)}]
    images = list(painting.images.all())
    sizes = painting.desired_sizes() if painting.status != Painting.AVAILABLE else []
    related = [
        p for p in painting.category.public_paintings().exclude(pk=painting.pk).prefetch_related("images")[:8]
        if p.url(lang)
    ][:4]
    main = images[0] if images else None
    context = {
        "painting": painting,
        "images": images,
        "crumbs": crumbs,
        "desired_sizes": sizes,
        "related": related,
        "description": painting.description(lang),
    }
    context["meta"] = build_meta(
        request, painting, h1=painting.t.title, fallback_description=painting.t.short or painting.description(lang),
        breadcrumbs=crumbs, og_image_url=main.image.url if main else "",
        noindex=getattr(request, "is_preview", False),
    )
    return render(request, "catalog/painting.html", context)


def common_sizes():
    return [size_option(s) for s in StandardSize.objects.filter(visible=True)]
