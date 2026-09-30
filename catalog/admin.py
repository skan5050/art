from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from unfold.admin import ModelAdmin, TabularInline

from core.admin import SEO_FIELDSET, site_link, thumb
from core.models import SharedBlock

from .models import Category, Painting, PaintingImage, PaintingSize, Technique


def tree_order():
    """Рубрики в порядке дерева с глубиной вложенности."""
    all_cats = list(Category.objects.all().order_by("order", "name_ru"))
    by_parent = {}
    for cat in all_cats:
        by_parent.setdefault(cat.parent_id, []).append(cat)
    result = []

    def walk(parent_id, depth):
        for cat in by_parent.get(parent_id, []):
            result.append((cat, depth))
            walk(cat.pk, depth + 1)

    walk(None, 0)
    return result


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "parent" in self.fields:
            excluded = set()
            if self.instance.pk:
                excluded = {self.instance.pk, *self.instance.descendant_ids()}
            choices = [("", "— верхний уровень —")]
            for cat, depth in tree_order():
                if cat.pk not in excluded:
                    choices.append((cat.pk, "— " * depth + cat.name_ru))
            self.fields["parent"].choices = choices


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    form = CategoryAdminForm
    list_display = ("tree_name", "cover_thumb", "works_count", "order", "visible", "link")
    list_editable = ("order", "visible")
    search_fields = ("name_ru", "name_en", "slug_ru")
    readonly_fields = ("cover_preview", "path_ru", "path_en")
    fieldsets = (
        (None, {"fields": ("parent", ("name_ru", "name_en"), ("slug_ru", "slug_en"), ("path_ru", "path_en"), ("intro_ru", "intro_en"),
                           ("caption_ru", "caption_en"), ("cta_text_ru", "cta_text_en"), ("cta_button_ru", "cta_button_en"), "order", "visible")}),
        ("Обложка", {"fields": ("cover", "cover_preview", ("cover_alt_ru", "cover_alt_en"), ("focus_x", "focus_y")),
                     "description": "Обложка заполняет плитку с обрезкой; точка фокуса задает, какая часть изображения остается видимой."}),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        self._depths = {cat.pk: depth for cat, depth in tree_order()}
        return super().get_queryset(request).select_related("parent")

    def get_ordering(self, request):
        from django.db.models import Case, IntegerField, Value, When

        order = tree_order()
        if not order:
            return ("order", "name_ru")
        return [Case(*[When(pk=cat.pk, then=Value(i)) for i, (cat, _) in enumerate(order)], output_field=IntegerField()).asc()]

    @admin.display(description="Рубрика")
    def tree_name(self, obj):
        depth = getattr(self, "_depths", {}).get(obj.pk, 0)
        return format_html('<span style="padding-left:{}px">{}{}</span>', depth * 22, "↳ " if depth else "", obj.name_ru)

    @admin.display(description="Обложка")
    def cover_thumb(self, obj):
        return thumb(obj.cover, 48)

    @admin.display(description="Предпросмотр")
    def cover_preview(self, obj):
        if not obj.cover:
            return "—"
        from core.images import thumbnail_url

        return format_html(
            '<div style="width:240px;aspect-ratio:4/3;overflow:hidden;border:1px solid #ddd">'
            '<img src="{}" style="width:100%;height:100%;object-fit:cover;object-position:{}% {}%" alt=""></div>',
            thumbnail_url(obj.cover, 480), obj.focus_x, obj.focus_y,
        )

    @admin.display(description="Работ")
    def works_count(self, obj):
        return obj.paintings.count()

    @admin.display(description="На сайте")
    def link(self, obj):
        return site_link(obj)

    # Удаление непустой рубрики: сначала выбрать, куда перенести содержимое.
    def get_urls(self):
        return [
            path("<int:pk>/move-and-delete/", self.admin_site.admin_view(self.move_and_delete), name="catalog_category_move_delete"),
        ] + super().get_urls()

    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and (obj.children.exists() or obj.paintings.exists()):
            return HttpResponseRedirect(reverse("admin:catalog_category_move_delete", args=[obj.pk]))
        return super().delete_view(request, object_id, extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    # Рабочий экран «Рубрики каталога» по макету: дерево слева, свойства выбранной рубрики справа.
    # Таблица с порядком и видимостью доступна по ссылке (?table=1).
    def changelist_view(self, request, extra_context=None):
        if "table" in request.GET:
            params = request.GET.copy()
            params.pop("table")
            request.GET = params
        elif request.method == "GET" and not request.GET:
            first = next(iter(tree_order()), None)
            if first:
                return HttpResponseRedirect(reverse("admin:catalog_category_change", args=[first[0].pk]))
        return super().changelist_view(request, extra_context)

    def _tree_context(self, current_pk=None):
        return {
            "pl_tree": [{"name": c.name_ru, "depth": d, "visible": c.visible, "current": c.pk == current_pk,
                         "url": reverse("admin:catalog_category_change", args=[c.pk])} for c, d in tree_order()],
            "pl_add_url": reverse("admin:catalog_category_add"),
            "pl_table_url": reverse("admin:catalog_category_changelist") + "?table=1",
        }

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra = {**self._tree_context(int(object_id) if str(object_id).isdigit() else None), **(extra_context or {})}
        return super().change_view(request, object_id, form_url, extra)

    def add_view(self, request, form_url="", extra_context=None):
        return super().add_view(request, form_url, {**self._tree_context(), **(extra_context or {})})

    def move_and_delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        excluded = {category.pk, *category.descendant_ids()}
        targets = [(c, d) for c, d in tree_order() if c.pk not in excluded]
        if request.method == "POST":
            target_id = request.POST.get("target")
            target = Category.objects.filter(pk=target_id).exclude(pk__in=excluded).first() if target_id else None
            move_children_to_root = request.POST.get("target") == "root"
            if target is None and not move_children_to_root:
                messages.error(request, "Выберите рубрику для переноса.")
            elif category.paintings.exists() and target is None:
                messages.error(request, "Картины нельзя оставить без рубрики — выберите рубрику.")
            else:
                with transaction.atomic():
                    moved = category.paintings.update(category=target) if target else 0
                    for child in category.children.all():
                        child.parent = target
                        child.save()
                    name = category.name_ru
                    category.delete()
                messages.success(request, f"Рубрика «{name}» удалена. Перенесено картин: {moved}.")
                return HttpResponseRedirect(reverse("admin:catalog_category_changelist"))
        return render(request, "admin/catalog/move_and_delete.html", {
            **self.admin_site.each_context(request),
            "title": f"Удаление рубрики «{category.name_ru}»",
            "category": category,
            "targets": [(c.pk, "— " * d + c.name_ru) for c, d in targets],
            "children": category.children.all(),
            "paintings_count": category.paintings.count(),
            "opts": self.model._meta,
        })


@admin.register(Technique)
class TechniqueAdmin(ModelAdmin):
    list_display = ("name_ru", "name_en", "order")
    list_editable = ("order",)


class PaintingImageInline(TabularInline):
    model = PaintingImage
    extra = 1
    fields = ("preview", "image", "alt_ru", "alt_en", "caption_ru", "caption_en", "order")
    readonly_fields = ("preview",)

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.image, 80)


class PaintingSizeInline(TabularInline):
    model = PaintingSize
    extra = 0
    fields = ("standard", "width", "height", "order")
    verbose_name_plural = "Свои размеры — действуют только при режиме «Свои размеры»"


class PaintingAdminForm(forms.ModelForm):
    class Meta:
        model = Painting
        fields = "__all__"
        widgets = {"sizes_mode": forms.RadioSelect, "description_mode": forms.RadioSelect, "status": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "category" in self.fields:
            self.fields["category"].choices = [("", "———")] + [(c.pk, "— " * d + c.name_ru) for c, d in tree_order()]


@admin.register(Painting)
class PaintingAdmin(ModelAdmin):
    form = PaintingAdminForm
    list_display = ("image_thumb", "title_ru", "category", "status", "published", "has_en", "link")
    list_display_links = ("image_thumb", "title_ru")
    list_filter = ("status", "published", "category", "technique", "sizes_mode", "description_mode")
    list_editable = ("status", "published")
    search_fields = ("title_ru", "title_en", "sku", "slug_ru")
    readonly_fields = ("description_source", "path_ru", "path_en", "sizes_preview")
    inlines = [PaintingImageInline, PaintingSizeInline]
    actions = ["make_available", "make_custom", "make_sold", "publish", "unpublish", "use_common_sizes"]
    save_on_top = True
    fieldsets = (
        (None, {"fields": (
            ("title_ru", "title_en"), ("status", "price"), ("category", "technique"), ("width", "height"), ("base_ru", "base_en"), "published",
        ), "description": "Фото, состояние, рубрика, цена и описание меняются в одной карточке. Заполняйте только известные значения — неизвестные не показываются на сайте."}),
        ("Описание", {"fields": (
            ("short_ru", "short_en"), "description_mode", "description_source", ("description_ru", "description_en"),
        )}),
        ("Дополнительно об оригинале", {"fields": (("framing_ru", "framing_en"), ("author_ru", "author_en"), "year")}),
        ("Желаемые размеры новой картины", {"fields": ("sizes_mode", "sizes_preview"),
            "description": "«Общий список» — ссылка на «Настройки сайта → Размеры картин». «Свои размеры» — список ниже, в блоке «Свои размеры». Это не фактический размер оригинала."}),
        ("Адрес и артикул", {"fields": (("slug_ru", "slug_en"), ("path_ru", "path_en"), "sku"), "classes": ("collapse",)}),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category").prefetch_related("images")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra = dict(extra_context or {})
        obj = self.get_object(request, object_id)
        if obj:
            extra["pl_preview_url"] = obj.url("ru") or ""
            image = obj.main_image()
            if image:
                from core.images import thumbnail_url

                extra["pl_photo_url"] = thumbnail_url(image.image, 720)
        return super().change_view(request, object_id, form_url, extra)

    @admin.display(description="Фото")
    def image_thumb(self, obj):
        image = obj.main_image()
        return thumb(image.image if image else None, 56)

    @admin.display(description="EN", boolean=True)
    def has_en(self, obj):
        return bool(obj.path_en)

    @admin.display(description="На сайте")
    def link(self, obj):
        return site_link(obj)

    @admin.display(description="Действующий источник текста")
    def description_source(self, obj):
        if obj.pk and obj.description_mode == Painting.DESC_OWN:
            return "Индивидуальное описание этой картины (общий текст на нее не влияет)."
        block = SharedBlock.objects.filter(key="painting-description").first()
        url = reverse("admin:core_sharedblock_change", args=[block.pk]) if block else ""
        text = block.text_ru if block else ""
        return format_html('Общий текст описания: «{}» — <a href="{}">изменить общий текст</a>', text, url)

    @admin.display(description="Список, который увидит посетитель")
    def sizes_preview(self, obj):
        if not obj.pk:
            return "Общий список (по умолчанию)"
        options = obj.desired_sizes()
        if not options:
            return "Список пуст"
        return format_html_join(", ", "{} см", ((o["label"],) for o in options))

    @admin.action(description="Состояние: В наличии")
    def make_available(self, request, queryset):
        for p in queryset:
            p.status = Painting.AVAILABLE
            p.save()

    @admin.action(description="Состояние: Под заказ")
    def make_custom(self, request, queryset):
        for p in queryset:
            p.status = Painting.CUSTOM
            p.save()

    @admin.action(description="Состояние: Продана (SOLD)")
    def make_sold(self, request, queryset):
        for p in queryset:
            p.status = Painting.SOLD
            p.save()

    @admin.action(description="Опубликовать")
    def publish(self, request, queryset):
        queryset.update(published=True)

    @admin.action(description="Снять с публикации")
    def unpublish(self, request, queryset):
        queryset.update(published=False)

    @admin.action(description="Вернуть общий список размеров")
    def use_common_sizes(self, request, queryset):
        queryset.update(sizes_mode=Painting.SIZES_COMMON)
