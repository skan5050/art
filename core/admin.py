from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import ROBOTS_DEFAULT, Label, Messenger, Redirect, SeoTemplate, SharedBlock, SiteSettings, StandardSize


def thumb(image, size=64):
    if not image:
        return "—"
    try:
        from .images import thumbnail_url

        url = thumbnail_url(image, 240)
    except Exception:  # noqa: BLE001
        url = image.url
    return format_html('<img src="{}" style="max-width:{}px;max-height:{}px;object-fit:contain;background:#f3f3f3" alt="">', url, size, size)


def site_link(obj, lang="ru"):
    url = obj.url(lang) if hasattr(obj, "url") else ""
    if not url:
        return "—"
    return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, url)


class SiteSettingsForm(forms.ModelForm):
    restore_robots = forms.BooleanField(
        label="Восстановить базовую версию robots.txt", required=False,
        help_text="Отметьте и сохраните, чтобы вернуть стандартный текст.",
    )

    class Meta:
        model = SiteSettings
        fields = "__all__"
        widgets = {"robots_txt": forms.Textarea(attrs={"rows": 10, "style": "font-family:monospace;width:100%"})}

    def clean(self):
        data = super().clean()
        if data.get("restore_robots"):
            data["robots_txt"] = ROBOTS_DEFAULT
            self.instance.robots_txt = ROBOTS_DEFAULT
            self.errors.pop("robots_txt", None)
        return data


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    readonly_fields = ("robots_preview", "sitemap_info")
    fieldsets = (
        ("Бренд", {"fields": (
            ("brand_name_ru", "brand_name_en"), ("slogan_ru", "slogan_en"), "logo", "logo_on_dark",
            ("logo_alt_ru", "logo_alt_en"), "logo_contains_slogan", "favicon",
        )}),
        ("Адрес сайта", {"fields": ("base_url",)}),
        ("Контакты", {"fields": (
            "phone", "email", ("address_ru", "address_en"), ("hours_ru", "hours_en"), ("geography_ru", "geography_en"),
        ), "description": "Мессенджеры настраиваются в разделе «Мессенджеры и каналы связи»."}),
        ("Футер", {"fields": (("copyright_ru", "copyright_en"),)}),
        ("Каталог", {"fields": ("show_sold_in_catalog", ("painting_prefix_ru", "painting_prefix_en"), "per_page", "currency")}),
        ("Подарочный сертификат", {"fields": (
            "certificate_image", "certificate_custom_amount", "certificate_electronic", "certificate_print",
        ), "description": "Номиналы — в разделе «Номиналы сертификата»."}),
        ("Карта продаж", {"fields": ("map_tiles_url", "map_attribution"), "classes": ("collapse",)}),
        ("Уведомления о заявках", {"fields": ("notify_emails",)}),
        ("SEO: robots.txt и sitemap.xml", {"fields": (
            "robots_txt", "restore_robots", "robots_disallow_all_confirmed", "robots_preview", "sitemap_info",
        )}),
        ("Поисковые панели и счетчики", {"fields": (
            "yandex_verification", "google_verification", "analytics_enabled", "yandex_metrika_id", "ga4_id",
        )}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.get()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))

    @admin.display(description="Итоговый robots.txt")
    def robots_preview(self, obj):
        return format_html('<pre style="background:#f6f6f6;padding:8px">{}</pre><a href="/robots.txt" target="_blank">Открыть /robots.txt</a>', obj.rendered_robots())

    @admin.display(description="sitemap.xml")
    def sitemap_info(self, obj):
        from .sitemap import sitemap_entries

        count = len(sitemap_entries())
        when = obj.sitemap_generated_at.strftime("%d.%m.%Y %H:%M") if obj.sitemap_generated_at else "еще не запрашивался"
        return format_html(
            '<a href="/sitemap.xml" target="_blank">/sitemap.xml</a> — обновляется автоматически. Адресов: {}. Последнее обращение: {}.',
            count, when,
        )


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("key", "value_ru", "value_en", "hint")
    list_editable = ("value_ru", "value_en")
    list_filter = ("group",)
    search_fields = ("key", "value_ru", "value_en", "hint")
    readonly_fields = ("key", "group", "hint")
    list_per_page = 200
    formfield_overrides = {}

    def get_changelist_formset(self, request, **kwargs):
        kwargs["widgets"] = {
            "value_ru": forms.Textarea(attrs={"rows": 2, "cols": 40}),
            "value_en": forms.Textarea(attrs={"rows": 2, "cols": 40}),
        }
        return super().get_changelist_formset(request, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SharedBlock)
class SharedBlockAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "usage", "visible")
    list_editable = ("visible",)
    search_fields = ("name", "key", "text_ru", "text_en")
    readonly_fields = ("key", "usage")
    fields = ("name", "key", "usage", ("title_ru", "title_en"), ("text_ru", "text_en"), ("button_ru", "button_en"), "visible")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "url", "order", "visible")
    list_editable = ("order", "visible")


@admin.register(StandardSize)
class StandardSizeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "group", "order", "visible")
    list_editable = ("order", "visible")
    list_filter = ("group", "visible")


@admin.register(SeoTemplate)
class SeoTemplateAdmin(admin.ModelAdmin):
    list_display = ("kind", "title_ru", "title_en")
    fields = ("kind", ("title_ru", "title_en"), ("description_ru", "description_en"))
    readonly_fields = ("kind",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ("old_path", "new_path", "created_at")
    search_fields = ("old_path", "new_path")


SEO_FIELDSET = ("SEO", {
    "classes": ("collapse",),
    "fields": (
        ("seo_title_ru", "seo_title_en"), ("seo_description_ru", "seo_description_en"), "indexable",
        ("og_title_ru", "og_title_en"), ("og_description_ru", "og_description_en"), "og_image",
    ),
    "description": "Title собирается как «Бренд | SEO Title». Пустые поля заполняются по шаблону типа страницы.",
})
