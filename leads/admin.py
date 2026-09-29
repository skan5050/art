from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Lead, LeadAttachment


class AttachmentInline(TabularInline):
    model = LeadAttachment
    extra = 0
    fields = ("link", "original_name", "size")
    readonly_fields = ("link", "original_name", "size")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="Файл")
    def link(self, obj):
        url = f"/{settings.ADMIN_PATH}private/{obj.file.name}"
        return format_html('<a href="{}" target="_blank"><img src="{}" style="max-height:120px" alt=""></a>', url, url)


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ("id", "created_at", "status", "kind", "name", "contact_line", "context", "notification_ok")
    list_display_links = ("id", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "kind", "lang", "created_at")
    search_fields = ("name", "contact", "comment", "painting_title", "city")
    inlines = [AttachmentInline]
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_at", "kind", "lang", "painting_link", "painting_title", "painting_status", "category", "source_link",
        "name", "contact_method", "contact", "city", "deadline", "comment", "size_display",
        "certificate_amount", "certificate_format", "certificate_recipient", "consent_given", "notification_error",
    )
    fieldsets = (
        ("Обработка", {"fields": ("status", "manager_note")}),
        ("Контакт", {"fields": ("name", "contact_method", "contact", "city")}),
        ("Контекст обращения", {"fields": ("kind", "painting_link", "painting_title", "painting_status", "category", "source_link", "lang", "created_at")}),
        ("Пожелания", {"fields": ("size_display", "deadline", "comment", "certificate_amount", "certificate_format", "certificate_recipient")}),
        ("Согласие", {"fields": ("consent_given",)}),
        ("Служебное", {"fields": ("notification_error",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        return False

    @admin.display(description="Контакт")
    def contact_line(self, obj):
        return f"{obj.get_contact_method_display()}: {obj.contact}"

    @admin.display(description="О чем")
    def context(self, obj):
        return obj.painting_title or (obj.category.name_ru if obj.category else "") or "—"

    @admin.display(description="Уведомление", boolean=True)
    def notification_ok(self, obj):
        return not obj.notification_error

    @admin.display(description="Картина")
    def painting_link(self, obj):
        if not obj.painting:
            return "—"
        return format_html('<a href="{}" target="_blank">{}</a>', obj.painting.url("ru"), obj.painting.title_ru)

    @admin.display(description="Страница")
    def source_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.source_url, obj.source_url) if obj.source_url else "—"
