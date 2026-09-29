from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "country_ru", "region", "population", "sale_confirmed", "visible", "caption_ru")
    list_editable = ("sale_confirmed", "visible")
    list_filter = ("sale_confirmed", "visible", "country_ru", "is_capital", "is_admin_center", "name_ru_verified")
    search_fields = ("name_ru", "name_en", "name_source", "region")
    list_per_page = 50
    readonly_fields = ("source", "source_id", "loaded_at")
    fieldsets = (
        ("Отметка на карте продаж", {"fields": ("sale_confirmed", "visible", ("caption_ru", "caption_en")),
            "description": "Карта показывает только подтвержденные продажи. Данные покупателей не указываются."}),
        ("Город", {"fields": (("name_ru", "name_en"), "name_source", "name_ru_verified", ("country_code", "country_ru", "country_en"), "region",
                              ("latitude", "longitude"), ("population", "population_date"), ("is_capital", "is_admin_center"))}),
        ("Происхождение записи", {"fields": ("source", "source_id", "loaded_at", "manually_edited"), "classes": ("collapse",)}),
    )

    def save_model(self, request, obj, form, change):
        city_fields = {"name_ru", "name_en", "latitude", "longitude", "population", "region", "country_ru"}
        if change and city_fields & set(form.changed_data):
            obj.manually_edited = True
        super().save_model(request, obj, form, change)
