from django.conf import settings as dj_settings
from django.contrib import admin, messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import path, reverse
from unfold.admin import ModelAdmin

from .models import City


@admin.register(City)
class CityAdmin(ModelAdmin):
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

    # Рабочий экран «Города на карте» по макету: список отмеченных городов, точка и превью карты.
    # Полный справочник (фильтры, страны, происхождение записей) остается в обычной таблице.
    def get_urls(self):
        wrap = self.admin_site.admin_view
        return [
            path("map/", wrap(self.map_view), name="geo_city_map"),
            path("map/search/", wrap(self.map_search), name="geo_city_map_search"),
        ] + super().get_urls()

    @staticmethod
    def _row(city):
        return {"id": city.pk, "name": city.name_ru, "country": city.country_ru, "region": city.region, "lat": float(city.latitude) if city.latitude is not None else None, "lng": float(city.longitude) if city.longitude is not None else None,
                "caption_ru": city.caption_ru, "caption_en": city.caption_en, "visible": city.visible, "on": city.sale_confirmed}

    def map_search(self, request):
        q = (request.GET.get("q") or "").strip()
        if len(q) < 2:
            return JsonResponse({"results": []})
        # SQLite сравнивает кириллицу с учетом регистра — ищем по нескольким написаниям.
        query = Q()
        for variant in {q, q.lower(), q.capitalize(), q.title(), q.upper()}:
            query |= Q(name_ru__icontains=variant) | Q(name_en__icontains=variant)
        found = City.objects.filter(query).order_by("-population")[:12]
        return JsonResponse({"results": [self._row(c) for c in found]})

    def map_view(self, request):
        if request.method == "POST":
            if not self.has_change_permission(request):
                return HttpResponseRedirect(request.path)
            ids = [int(x) for x in request.POST.getlist("row") if x.isdigit()]
            with transaction.atomic():
                for city in City.objects.filter(pk__in=ids):
                    on = bool(request.POST.get(f"on_{city.pk}"))
                    visible = bool(request.POST.get(f"visible_{city.pk}"))
                    caption_ru = request.POST.get(f"caption_ru_{city.pk}", city.caption_ru).strip()[:200]
                    caption_en = request.POST.get(f"caption_en_{city.pk}", city.caption_en).strip()[:200]
                    if (on, visible, caption_ru, caption_en) != (city.sale_confirmed, city.visible, city.caption_ru, city.caption_en):
                        city.sale_confirmed, city.visible, city.caption_ru, city.caption_en = on, visible, caption_ru, caption_en
                        city.save()
            messages.success(request, "Отметки сохранены.")
            return HttpResponseRedirect(request.path)
        rows = [self._row(c) for c in City.objects.filter(sale_confirmed=True).order_by("name_ru")]
        return render(request, "admin/geo/city/sales_map.html", {
            **self.admin_site.each_context(request),
            "title": "Города продаж", "opts": self.model._meta, "rows": rows, "theme_d": dj_settings.SITE_THEME == "d",
            "geo_url": static("geo/countries.json"), "table_url": reverse("admin:geo_city_changelist"),
            "search_url": reverse("admin:geo_city_map_search"), "add_url": reverse("admin:geo_city_add"),
        })
