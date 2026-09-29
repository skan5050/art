from django.contrib import admin

from core.admin import SEO_FIELDSET, site_link, thumb

from .models import Article, CertificateNominal, HomeSection, MenuItem, Page, Review, StudioImage


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
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
            ("intro_ru", "intro_en"), ("body_ru", "body_en"), ("note_ru", "note_en"), ("empty_ru", "empty_en"),
            ("button_ru", "button_en"), "image", ("image_alt_ru", "image_alt_en"),
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
class ArticleAdmin(admin.ModelAdmin):
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
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "page", "url", "order", "visible", "in_footer")
    list_editable = ("order", "visible", "in_footer")
    fields = (("label_ru", "label_en"), "page", "url", "order", "visible", "in_footer")


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ("kind", "title_ru", "order", "visible")
    list_editable = ("order", "visible")
    filter_horizontal = ("paintings",)
    fields = ("kind", ("title_ru", "title_en"), ("text_ru", "text_en"), ("button_ru", "button_en"), "image", "paintings", "limit", "order", "visible")
    readonly_fields = ("kind",)

    def has_add_permission(self, request):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_ru", "short_text", "photo_thumb", "published", "order")
    list_editable = ("published", "order")
    fields = (("text_ru", "text_en"), ("author_ru", "author_en"), ("city_ru", "city_en"), "photo", "painting", "published", "order")
    autocomplete_fields = ("painting",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text_ru[:80]

    @admin.display(description="Фото")
    def photo_thumb(self, obj):
        return thumb(obj.photo, 48)


@admin.register(CertificateNominal)
class CertificateNominalAdmin(admin.ModelAdmin):
    list_display = ("__str__", "label_ru", "order", "visible")
    list_editable = ("order", "visible")


@admin.register(StudioImage)
class StudioImageAdmin(admin.ModelAdmin):
    list_display = ("preview", "caption_ru", "is_illustration", "order", "visible")
    list_editable = ("order", "visible")
    fields = ("image", ("alt_ru", "alt_en"), ("caption_ru", "caption_en"), "is_illustration", "order", "visible")

    @admin.display(description="Изображение")
    def preview(self, obj):
        return thumb(obj.image, 64)
