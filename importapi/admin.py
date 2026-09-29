from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import ApiKey, ImportLog, ImportRecord
from .services import assign_record_to_painting, create_card_from_record


class ApiKeyForm(forms.ModelForm):
    class Meta:
        model = ApiKey
        fields = ("name", "can_replace_cover", "can_create_cards", "can_publish")


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    form = ApiKeyForm
    list_display = ("name", "prefix", "permissions", "created_at", "last_used_at", "state")
    readonly_fields = ("prefix", "created_at", "last_used_at", "revoked_at")
    actions = ["revoke"]

    def get_fields(self, request, obj=None):
        if obj is None:
            return ("name", "can_replace_cover", "can_create_cards", "can_publish")
        return ("name", "prefix", "can_replace_cover", "can_create_cards", "can_publish", "created_at", "last_used_at", "revoked_at")

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
            return
        key, token = ApiKey.issue(
            obj.name, can_replace_cover=obj.can_replace_cover, can_create_cards=obj.can_create_cards, can_publish=obj.can_publish,
        )
        obj.pk = key.pk
        obj.prefix = key.prefix
        messages.warning(
            request,
            format_html(
                "Ключ создан. Скопируйте его сейчас — больше он показан не будет:<br>"
                '<code style="font-size:14px;user-select:all">{}</code>', token,
            ),
        )

    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        return HttpResponseRedirect(reverse("admin:importapi_apikey_changelist"))

    @admin.display(description="Разрешения")
    def permissions(self, obj):
        perms = ["загрузка фото"]
        if obj.can_replace_cover:
            perms.append("обложки")
        if obj.can_create_cards:
            perms.append("карточки-черновики")
        if obj.can_publish:
            perms.append("публикация")
        return ", ".join(perms)

    @admin.display(description="Состояние")
    def state(self, obj):
        return "Действует" if obj.is_active else f"Отозван {obj.revoked_at:%d.%m.%Y}"

    @admin.action(description="Отозвать выбранные ключи")
    def revoke(self, request, queryset):
        for key in queryset:
            key.revoke()
        messages.success(request, "Ключи отозваны. Новые запросы с ними отклоняются; загруженные файлы сохранены.")


class ImportRecordForm(forms.ModelForm):
    assign_to = forms.ModelChoiceField(
        queryset=None, required=False, label="Назначить картине",
        help_text="Фото будет добавлено в галерею выбранной картины.",
    )

    class Meta:
        model = ImportRecord
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from catalog.models import Painting

        self.fields["assign_to"].queryset = Painting.objects.all()


@admin.register(ImportRecord)
class ImportRecordAdmin(admin.ModelAdmin):
    form = ImportRecordForm
    list_display = ("preview", "external_id", "category", "purpose", "state", "painting", "created_at")
    list_filter = ("state", "purpose", "category")
    search_fields = ("external_id", "original_name")
    readonly_fields = ("preview_large", "external_id", "category", "purpose", "state", "original_name", "width", "height", "painting", "api_key", "created_at")
    actions = ["create_drafts"]

    def get_fields(self, request, obj=None):
        return ("preview_large", "external_id", "category", "purpose", "state", "original_name", ("width", "height"), "painting", "assign_to", "api_key", "created_at")

    def has_add_permission(self, request):
        return False

    def _url(self, obj):
        from django.conf import settings

        return f"/{settings.ADMIN_PATH}private/{obj.file.name}"

    @admin.display(description="Фото")
    def preview(self, obj):
        return format_html('<img src="{}" style="max-height:56px" alt="">', self._url(obj))

    @admin.display(description="Фото")
    def preview_large(self, obj):
        return format_html('<img src="{}" style="max-height:320px" alt="">', self._url(obj))

    def save_model(self, request, obj, form, change):
        painting = form.cleaned_data.get("assign_to")
        if painting:
            assign_record_to_painting(obj, painting)
            messages.success(request, f"Фото добавлено к картине «{painting}».")

    @admin.action(description="Создать карточки-черновики с общим описанием")
    def create_drafts(self, request, queryset):
        created = 0
        for record in queryset.filter(state="accepted", purpose="photo", category__isnull=False):
            create_card_from_record(record, publish=False)
            created += 1
        messages.success(request, f"Создано черновиков: {created}. Проверьте названия и характеристики перед публикацией.")


@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "key_prefix", "action", "external_id", "category_id_value", "file_name", "result", "message")
    list_filter = ("result", "action", "key_prefix")
    search_fields = ("external_id", "file_name", "message")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
