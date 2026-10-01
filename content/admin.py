from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from core.admin import SEO_FIELDSET, site_link, thumb

from .models import (Article, CertificateNominal, CityLanding, CooperationAdvantage, CooperationBlock, CooperationContent, HomeSection,
                     MediaAsset, MenuItem, Page, Review, StudioImage)


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ("title_ru", "kind", "link_ru", "link_en", "published", "order")
    list_editable = ("published", "order")
    list_filter = ("kind", "published")
    search_fields = ("title_ru", "title_en", "body_ru")
    readonly_fields = ("path_ru", "path_en")
    save_on_top = True

    def get_fieldsets(self, request, obj=None):
        main = (None, {"fields": (
            "kind", ("title_ru", "title_en"), ("nav_title_ru", "nav_title_en"), ("slug_ru", "slug_en"), ("path_ru", "path_en"),
            "published", "order",
        )})
        text = ("Тексты", {"fields": (
            ("kicker_ru", "kicker_en"), ("intro_ru", "intro_en"), ("body_ru", "body_en"), ("note_ru", "note_en"), ("empty_ru", "empty_en"),
            ("button_ru", "button_en"), ("cta_text_ru", "cta_text_en"), ("cta_button_ru", "cta_button_en"),
            "image", ("image_alt_ru", "image_alt_en"),
        )})
        banner = ("Баннер главной — все надписи редактируются здесь, а не в изображении", {"fields": (
            "banner_image", "banner_image_mobile", ("banner_focus_x", "banner_focus_y"),
            ("banner_kicker_ru", "banner_kicker_en"), ("banner_title_ru", "banner_title_en"), ("banner_text_ru", "banner_text_en"),
            ("banner_button1_ru", "banner_button1_en"), "banner_button1_link", ("banner_button2_ru", "banner_button2_en"),
        )})
        if obj is not None and obj.kind == "home":
            return (main, banner, text, SEO_FIELDSET)
        return (main, text, SEO_FIELDSET)

    @admin.display(description="Адрес RU")
    def link_ru(self, obj):
        return site_link(obj, "ru")

    @admin.display(description="Адрес EN")
    def link_en(self, obj):
        return site_link(obj, "en")


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ("title_ru", "link_ru", "link_en", "published", "order", "published_at")
    list_editable = ("published", "order")
    list_filter = ("published",)
    search_fields = ("title_ru", "title_en", "body_ru", "body_en")
    readonly_fields = ("path_ru", "path_en")
    filter_horizontal = ("related_categories", "related_paintings")
    save_on_top = True
    fieldsets = (
        (None, {"fields": (("title_ru", "title_en"), ("slug_ru", "slug_en"), ("path_ru", "path_en"), "published", "published_at", "order")}),
        ("Текст", {"fields": (("excerpt_ru", "excerpt_en"), ("body_ru", "body_en"), ("button_ru", "button_en"), "cover", ("cover_alt_ru", "cover_alt_en"))}),
        ("Ссылки на каталог", {"fields": ("related_categories", "related_paintings"), "classes": ("collapse",)}),
        SEO_FIELDSET,
    )

    @admin.display(description="Адрес RU")
    def link_ru(self, obj):
        return site_link(obj, "ru")

    @admin.display(description="Адрес EN")
    def link_en(self, obj):
        return site_link(obj, "en")


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ("__str__", "page", "url", "order", "visible", "in_footer")
    list_editable = ("order", "visible", "in_footer")
    fields = (("label_ru", "label_en"), "page", "url", "order", "visible", "in_footer")

    # Рабочий экран «Меню сайта» по макету: строки с перетаскиванием, видимость, удаление, предпросмотр.
    # Обычная таблица доступна по ссылке «Таблица» (?table=1) — прежние возможности сохранены.
    def changelist_view(self, request, extra_context=None):
        if "table" in request.GET or request.GET.keys() - {"e"}:
            if "table" in request.GET:
                params = request.GET.copy()
                params.pop("table")
                request.GET = params
            return super().changelist_view(request, extra_context)
        if request.method == "POST" and "menu_editor" in request.POST:
            return self.save_menu(request)
        items = list(MenuItem.objects.select_related("page").order_by("order", "id"))
        rows = [{"item": it, "link": it.page.path_ru if it.page else it.url, "label": str(it)} for it in items]
        from django.conf import settings as dj_settings

        from core.models import SiteSettings

        return render(request, "admin/content/menuitem/menu_editor.html", {
            **self.admin_site.each_context(request),
            "title": "Меню сайта", "rows": rows, "opts": self.model._meta, "site_settings": SiteSettings.get(),
            "theme_d": dj_settings.SITE_THEME == "d",
            "add_url": reverse("admin:content_menuitem_add"), "table_url": "?table=1",
        })

    def save_menu(self, request):
        if not self.has_change_permission(request):
            return HttpResponseRedirect(request.path)
        ids = [int(x) for x in request.POST.getlist("row") if x.isdigit()]
        with transaction.atomic():
            from core.models import SiteSettings

            flags = SiteSettings.get()
            if "flags" in request.POST:
                flags.menu_in_header = bool(request.POST.get("menu_in_header"))
                flags.menu_in_footer = bool(request.POST.get("menu_in_footer"))
                flags.save()
            for position, pk in enumerate(ids):
                item = MenuItem.objects.filter(pk=pk).first()
                if item is None:
                    continue
                if request.POST.get(f"delete_{pk}") and self.has_delete_permission(request, item):
                    item.delete()
                    continue
                item.order = position * 10
                item.label_ru = request.POST.get(f"label_ru_{pk}", item.label_ru).strip()[:60]
                item.label_en = request.POST.get(f"label_en_{pk}", item.label_en).strip()[:60]
                item.visible = bool(request.POST.get(f"visible_{pk}"))
                if f"footer_{pk}" in request.POST or f"footer_present_{pk}" in request.POST:
                    item.in_footer = bool(request.POST.get(f"footer_{pk}"))
                item.save()
        messages.success(request, "Меню сохранено.")
        return HttpResponseRedirect(request.path)


@admin.register(HomeSection)
class HomeSectionAdmin(ModelAdmin):
    list_display = ("kind", "title_ru", "order", "visible")
    list_editable = ("order", "visible")
    filter_horizontal = ("paintings",)
    fields = ("kind", ("kicker_ru", "kicker_en"), ("title_ru", "title_en"), ("text_ru", "text_en"), ("button_ru", "button_en"), "image", "paintings", "limit", "order", "visible")
    readonly_fields = ("kind",)

    def has_add_permission(self, request):
        return False


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("author_ru", "short_text", "photo_thumb", "published", "order")
    list_editable = ("published", "order")
    fields = (("text_ru", "text_en"), ("author_ru", "author_en"), ("city_ru", "city_en"), "date", "photo", "painting", "featured", "published", "order")
    autocomplete_fields = ("painting",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text_ru[:80]

    @admin.display(description="Фото")
    def photo_thumb(self, obj):
        return thumb(obj.photo, 48)


@admin.register(CertificateNominal)
class CertificateNominalAdmin(ModelAdmin):
    list_display = ("__str__", "label_ru", "order", "visible")
    list_editable = ("order", "visible")


@admin.register(StudioImage)
class StudioImageAdmin(ModelAdmin):
    list_display = ("preview", "caption_ru", "is_illustration", "order", "visible")
    list_editable = ("order", "visible")
    fields = ("image", ("alt_ru", "alt_en"), ("caption_ru", "caption_en"), "is_illustration", "order", "visible")

    @admin.display(description="Изображение")
    def preview(self, obj):
        return thumb(obj.image, 64)


@admin.register(MediaAsset)
class MediaAssetAdmin(ModelAdmin):
    list_display = ("preview", "title", "snippet_text", "uploaded_at")
    search_fields = ("title", "alt_ru", "alt_en")
    fields = ("image", "preview_large", "title", ("alt_ru", "alt_en"), ("caption_ru", "caption_en"), "snippet_text")
    readonly_fields = ("preview_large", "snippet_text")

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.image, 56)

    @admin.display(description="Предпросмотр")
    def preview_large(self, obj):
        return thumb(obj.image, 320)

    @admin.display(description="Вставка в текст")
    def snippet_text(self, obj):
        from django.utils.html import format_html

        if not obj.image:
            return "—"
        return format_html('<code style="user-select:all">{}</code><br><small>Скопируйте строку в текст страницы или статьи отдельным абзацем; на следующей строке можно добавить подпись.</small>', obj.snippet)


@admin.register(CityLanding)
class CityLandingAdmin(ModelAdmin):
    list_display = ("name_ru", "title_ru", "address_filled", "published", "order", "link")
    list_editable = ("published", "order")
    list_filter = ("published",)
    search_fields = ("name_ru", "title_ru", "address_ru")
    autocomplete_fields = ("city",)
    readonly_fields = ("path_ru", "path_en")
    fieldsets = (
        ("Город", {"fields": ("city", ("name_ru", "name_en"), "name_in_ru", "published", "show_in_picker", "geo_aliases", "order"),
                   "description": "Каждая городская страница пишется отдельно: свой текст, реальный адрес. Однотипные клоны не создаются (ТЗ 12.6)."}),
        ("Текст", {"fields": (("title_ru", "title_en"), ("intro_ru", "intro_en"), ("body_ru", "body_en"),
                              ("delivery_ru", "delivery_en"), ("button_ru", "button_en"), "cover", ("cover_alt_ru", "cover_alt_en"))}),
        ("Адрес и карта", {"fields": (("address_ru", "address_en"), ("address_lat", "address_lng"), ("hours_ru", "hours_en"), "phone"),
                           "description": "Без адреса и координат карта на странице не показывается."}),
        ("Адрес страницы", {"fields": (("slug_ru", "slug_en"), ("path_ru", "path_en"))}),
        SEO_FIELDSET,
    )

    @admin.display(description="Адрес", boolean=True)
    def address_filled(self, obj):
        return obj.has_map

    @admin.display(description="На сайте")
    def link(self, obj):
        return site_link(obj)



class CooperationBlockInline(StackedInline):
    model = CooperationBlock
    extra = 0
    max_num = 3
    can_delete = False  # блок скрывается галочкой «Показывать блок»; три блока заданы макетом
    fields = ("order", "visible", ("title_ru", "title_en"), ("text_ru", "text_en"), "image", "image_asset", "preview",
              ("alt_ru", "alt_en"), ("show_image", "image_side"), ("focus_x", "focus_y"))
    readonly_fields = ("preview",)
    autocomplete_fields = ("image_asset",)
    verbose_name = "Блок «текст + фото»"
    verbose_name_plural = "Три блока «текст + фото» (положение по умолчанию — как в утверждённом макете)"

    @admin.display(description="Сейчас на странице")
    def preview(self, obj):
        return thumb(obj.image_file) if obj and obj.pk and obj.image_file else "—"


class CooperationAdvantageInline(StackedInline):
    model = CooperationAdvantage
    extra = 0
    max_num = 8
    fields = (("order", "visible"), ("icon_key", "icon_file"), ("title_ru", "title_en"), ("text_ru", "text_en"))
    verbose_name = "Преимущество"
    verbose_name_plural = "Преимущества (остальные равномерно перераспределяются по строке)"


@admin.register(CooperationContent)
class CooperationAdmin(ModelAdmin):
    """Страница «Сотрудничество»: тексты, изображения, постер, блоки и преимущества. Оформление задано дизайном сайта."""

    inlines = [CooperationBlockInline, CooperationAdvantageInline]
    autocomplete_fields = ("hero_image_asset", "cta_image_asset")
    readonly_fields = ("page_link", "hero_preview", "cta_preview")
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("page_link",),
                "description": "Здесь редактируется содержимое. Адрес, SEO и пункт меню — в карточке страницы (ссылка ниже). "
                               "Сетка, шрифты, цвета, шапка и подвал фиксированы дизайном сайта и отсюда не меняются."}),
        ("Верхний постер", {"fields": ("hero_mode", ("hero_kicker_ru", "hero_kicker_en"), ("h1_ru", "h1_en"),
                                       ("hero_subtitle_ru", "hero_subtitle_en"), ("hero_lead_ru", "hero_lead_en"),
                                       ("hero_button_ru", "hero_button_en"), ("hero_button_action", "hero_button_url"))}),
        ("Фото постера", {"fields": ("hero_image", "hero_image_asset", "hero_preview", "hero_image_mobile",
                                     ("hero_image_alt_ru", "hero_image_alt_en"), "hero_show_image", ("hero_focus_x", "hero_focus_y"), "hero_overlay"),
                          "description": "Удалите фото (галочка «Очистить») — страница вернётся к фирменному фону дизайна. "
                                         "Текст постера остаётся HTML-текстом, в фото не вшивается."}),
        ("Финальный блок", {"fields": (("cta_title_ru", "cta_title_en"), ("cta_text_ru", "cta_text_en"), ("cta_button_ru", "cta_button_en"),
                                       ("cta_button_action", "cta_button_url"), "cta_image", "cta_image_asset", "cta_preview",
                                       ("cta_image_alt_ru", "cta_image_alt_en"), "cta_show_image", ("cta_focus_x", "cta_focus_y"))}),
        ("Заголовок блока преимуществ", {"fields": (("adv_title_ru", "adv_title_en"),)}),
    )

    def has_add_permission(self, request):
        return not CooperationContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = CooperationContent.get()  # одна запись на сайт: сразу открываем редактирование
        return HttpResponseRedirect(reverse("admin:content_cooperationcontent_change", args=[obj.pk]))

    @admin.display(description="Страница")
    def page_link(self, obj):
        from django.utils.html import format_html

        page = Page.objects.filter(kind="cooperation").first()
        if page is None:
            return "Страница ещё не создана: выполните seed_site или создайте страницу типа «Сотрудничество»."
        return format_html('<a href="{}">Адрес, SEO, публикация и меню — карточка страницы</a> · {}', reverse("admin:content_page_change", args=[page.pk]),
                           site_link(page, "ru"))

    @admin.display(description="Сейчас")
    def hero_preview(self, obj):
        return thumb(obj.hero_file) if obj and obj.hero_file else "—"

    @admin.display(description="Сейчас")
    def cta_preview(self, obj):
        return thumb(obj.cta_file) if obj and obj.cta_file else "—"
