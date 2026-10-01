from django.conf import settings as dj_settings
from django.utils import timezone

from .i18n import current_lang
from .models import Messenger, SiteSettings


def site(request):
    if request.path.startswith("/" + dj_settings.ADMIN_PATH):
        return {}
    from content.models import MenuItem, Page

    lang = current_lang()
    settings = SiteSettings.get()
    menu = [r for r in (item.resolved(lang) for item in MenuItem.objects.filter(visible=True).select_related("page")) if r]
    footer_menu = [
        r for r in (item.resolved(lang) for item in MenuItem.objects.filter(visible=True, in_footer=True).select_related("page")) if r
    ]
    if not settings.menu_in_header:
        menu = []
    if not settings.menu_in_footer:
        footer_menu = []
    pages = {p.kind: p for p in Page.objects.filter(published=True).exclude(kind="text")}
    service_pages = [p for p in Page.objects.filter(published=True, kind="text") if p.url(lang)]

    alternates = getattr(request, "alternate_urls", {}) or {}
    other = "ru" if lang == "en" else "en"
    brand = settings.brand(lang)
    year = timezone.localdate().year
    copyright_text = (settings.copyright_en if lang == "en" else settings.copyright_ru) or ""
    from catalog.views import common_sizes
    from content.models import CertificateNominal

    return {
        "theme_font_preload": "montserrat-cyrillic-400-normal.woff2" if dj_settings.SITE_THEME == "a" else "liberation-sans-400.woff2",
        "contact_methods": ["phone", "telegram", "whatsapp", "max", "email"],
        "common_sizes": common_sizes(),
        "certificate_nominals": list(CertificateNominal.objects.filter(visible=True)),
        "site": settings,
        "brand": brand,
        "slogan": settings.t.slogan,
        "lang": lang,
        "theme": dj_settings.SITE_THEME,
        "menu_items": menu,
        "footer_menu": footer_menu,
        "messengers": list(Messenger.objects.filter(visible=True)),
        "site_pages": {k: v for k, v in pages.items() if v.url(lang)},
        "service_pages": service_pages,
        "other_lang": other,
        "other_lang_url": alternates.get(other, ""),
        "home_url": "/en/" if lang == "en" else "/",
        "copyright_text": copyright_text.replace("{year}", str(year)).replace("{brand}", brand),
        "analytics": {
            "metrika": settings.yandex_metrika_id if settings.analytics_enabled else "",
            "ga4": settings.ga4_id if settings.analytics_enabled else "",
        },
    }
