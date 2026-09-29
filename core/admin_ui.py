"""Оформление админки: боковое меню, счетчики и рабочий экран «Сегодня в мастерской».

Подключается в settings.UNFOLD. Вид (цвета, логотип) меняется там же, без правок логики.
"""
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils import timezone


def perm(codename):
    return lambda request: request.user.has_perm(codename)


def changelist(app_model):
    app, model = app_model.split(".")
    return reverse_lazy(f"admin:{app}_{model}_changelist")


def item(title, icon, app_model, badge=None):
    app, model = app_model.split(".")
    entry = {"title": title, "icon": icon, "link": changelist(app_model), "permission": perm(f"{app}.view_{model}")}
    if badge:
        entry["badge"] = badge
    return entry


def new_leads_badge(request):
    from leads.models import Lead

    count = Lead.objects.filter(status="new").count()
    return str(count) if count else ""


def import_badge(request):
    from importapi.models import ImportRecord

    count = ImportRecord.objects.filter(state="accepted").count()
    return str(count) if count else ""


def environment_callback(request):
    site = "МираМе (A)" if settings.SITE_THEME == "a" else "ХолСтори (D)"
    return [site, "info" if not settings.DEBUG else "warning"]


def site_title(request):
    from core.models import SiteSettings

    return SiteSettings.get().brand_name_ru or "Сайт"


SIDEBAR = {
    "show_search": True,
    "show_all_applications": True,
    "navigation": [
        {"title": "Работа", "separator": False, "items": [
            {"title": "Сегодня в мастерской", "icon": "space_dashboard", "link": reverse_lazy("admin:index")},
            item("Заявки", "inbox", "leads.lead", badge="core.admin_ui.new_leads_badge"),
        ]},
        {"title": "Каталог", "separator": True, "collapsible": False, "items": [
            item("Картины", "palette", "catalog.painting"),
            item("Рубрики", "category", "catalog.category"),
            item("Техники", "brush", "catalog.technique"),
            item("Импорт: файлы", "cloud_upload", "importapi.importrecord", badge="core.admin_ui.import_badge"),
        ]},
        {"title": "Страницы и тексты", "separator": True, "collapsible": True, "items": [
            item("Страницы", "description", "content.page"),
            item("Главная: блоки", "home", "content.homesection"),
            item("Статьи «Полезное»", "article", "content.article"),
            item("Отзывы", "reviews", "content.review"),
            item("Меню", "menu", "content.menuitem"),
            item("Сертификаты: номиналы", "card_giftcard", "content.certificatenominal"),
            item("Мастерская: изображения", "photo_library", "content.studioimage"),
            item("Медиатека", "perm_media", "content.mediaasset"),
            item("Надписи интерфейса", "translate", "core.label"),
            item("Общие блоки", "view_agenda", "core.sharedblock"),
        ]},
        {"title": "Карта и SEO", "separator": True, "collapsible": True, "items": [
            item("Города на карте", "map", "geo.city"),
            item("SEO-шаблоны", "travel_explore", "core.seotemplate"),
            item("Перенаправления", "alt_route", "core.redirect"),
        ]},
        {"title": "Настройки", "separator": True, "collapsible": True, "items": [
            item("Настройки сайта", "settings", "core.sitesettings"),
            item("Мессенджеры", "chat", "core.messenger"),
            item("Стандартные размеры", "straighten", "core.standardsize"),
            item("API-ключи импорта", "key", "importapi.apikey"),
            item("Журнал импорта", "history", "importapi.importlog"),
            item("Пользователи", "person", "auth.user"),
            item("Группы и права", "group", "auth.group"),
        ]},
    ],
}


def _safe_reverse(name, *args):
    try:
        return reverse(name, args=args)
    except Exception:
        return ""


def site_checks():
    """Короткая проверка готовности сайта для рабочего экрана (без обхода страниц)."""
    from catalog.models import Painting
    from core.models import Messenger, SiteSettings
    from geo.models import City

    s = SiteSettings.get()
    checks = []

    def add(ok, title, hint, link=""):
        checks.append({"ok": ok, "title": title, "hint": hint, "link": link})

    settings_link = _safe_reverse("admin:core_sitesettings_changelist")
    has_contacts = bool(s.phone or s.email or Messenger.objects.filter(visible=True).exists())
    add(has_contacts, "Контакты заполнены" if has_contacts else "Контакты не заполнены", "Телефон, email или мессенджер — без них блоки контактов не выводятся.", settings_link)
    add(bool(s.notify_emails), "Почта для заявок указана" if s.notify_emails else "Не указана почта для заявок", "Куда отправлять уведомления о новых заявках.", settings_link)
    demo = Painting.objects.filter(sku__startswith="DEMO-").count()
    add(demo == 0, "Демо-работы удалены" if demo == 0 else f"Демо-работ на сайте: {demo}",
        "Удалите перед запуском: python manage.py seed_demo --remove", _safe_reverse("admin:catalog_painting_changelist") + "?q=DEMO-")
    published = Painting.objects.filter(published=True).exclude(sku__startswith="DEMO-").count()
    add(published > 0, f"Опубликованных работ: {published}", "Добавьте работы вручную или через API импорта.",
        _safe_reverse("admin:catalog_painting_add"))
    on_map = City.objects.filter(sale_confirmed=True, visible=True).count()
    add(on_map > 0, f"Городов на карте: {on_map}", "Отметки продаж на странице «Доставка» и в SOLD.", _safe_reverse("admin:geo_city_changelist"))
    gaps = translation_gaps()
    add(gaps == 0, "Переводы RU/EN заполнены" if gaps == 0 else f"Незаполненных переводов: {gaps}",
        "Подробный отчет: python manage.py audit_content", "")
    return checks


def translation_gaps():
    from django.apps import apps
    from django.db import models as dj

    total = 0
    for model in apps.get_models():
        if model._meta.app_label not in ("core", "catalog", "content"):
            continue
        names = {f.name for f in model._meta.get_fields() if isinstance(f, (dj.CharField, dj.TextField))}
        pairs = [n[:-3] for n in names if n.endswith("_ru") and f"{n[:-3]}_en" in names and n[:-3] not in ("path", "slug")]
        if not pairs:
            continue
        for obj in model.objects.all().only(*[f"{p}_ru" for p in pairs], *[f"{p}_en" for p in pairs]):
            if getattr(obj, "published", True) is False or getattr(obj, "visible", True) is False:
                continue
            for p in pairs:
                if bool((getattr(obj, f"{p}_ru") or "").strip()) != bool((getattr(obj, f"{p}_en") or "").strip()):
                    total += 1
    return total


STATUS_TONE = {"new": "new", "in_progress": "work", "closed": "done"}


def dashboard_callback(request, context):
    from catalog.models import Painting
    from content.models import Page
    from importapi.models import ImportRecord
    from leads.models import Lead

    now = timezone.localtime()
    leads = []
    for lead in Lead.objects.select_related("painting", "category").order_by("-created_at")[:8]:
        about = lead.painting_title or (lead.category.name_ru if lead.category else "")
        leads.append({
            "name": lead.name,
            "what": " · ".join(x for x in (lead.get_kind_display(), about) if x),
            "when": timezone.localtime(lead.created_at),
            "status": lead.get_status_display(),
            "tone": STATUS_TONE.get(lead.status, "new"),
            "url": reverse("admin:leads_lead_change", args=[lead.pk]),
        })
    home = Page.objects.filter(kind="home").first()
    banner = ""
    if home and home.banner_image:
        banner = home.banner_image.url
    lead_list = reverse("admin:leads_lead_changelist")
    painting_list = reverse("admin:catalog_painting_changelist")
    stats = [
        {"label": "Новые заявки", "value": Lead.objects.filter(status="new").count(), "url": f"{lead_list}?status__exact=new", "accent": True},
        {"label": "В работе", "value": Lead.objects.filter(status="in_progress").count(), "url": f"{lead_list}?status__exact=in_progress"},
        {"label": "Работ опубликовано", "value": Painting.objects.filter(published=True).count(), "url": f"{painting_list}?published__exact=1"},
        {"label": "Черновики", "value": Painting.objects.filter(published=False).count(), "url": f"{painting_list}?published__exact=0"},
        {"label": "Файлы импорта ждут", "value": ImportRecord.objects.filter(state="accepted").count(),
         "url": reverse("admin:importapi_importrecord_changelist") + "?state__exact=accepted"},
    ]
    actions = [
        ("Добавить картину", "add_photo_alternate", _safe_reverse("admin:catalog_painting_add")),
        ("Рубрики", "category", _safe_reverse("admin:catalog_category_changelist")),
        ("Отзывы", "reviews", _safe_reverse("admin:content_review_changelist")),
        ("Сертификаты", "card_giftcard", _safe_reverse("admin:content_certificatenominal_changelist")),
        ("Города на карте", "map", _safe_reverse("admin:geo_city_changelist")),
        ("Контакты и настройки", "settings", _safe_reverse("admin:core_sitesettings_changelist")),
    ]
    context.update({
        "today": now,
        "dash_leads": leads,
        "dash_stats": stats,
        "dash_actions": [{"title": t, "icon": i, "url": u} for t, i, u in actions if u],
        "dash_checks": site_checks(),
        "dash_home": {"banner": banner, "title": home.banner_title_ru if home else "",
                      "url": reverse("admin:content_page_change", args=[home.pk]) if home else ""},
        "dash_add_painting": _safe_reverse("admin:catalog_painting_add"),
        "dash_lead_list": lead_list,
    })
    return context


def admin_styles(request):
    return static("admin-ui/admin.css")


def admin_scripts(request):
    return static("admin-ui/admin.js")
