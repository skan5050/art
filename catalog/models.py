from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.i18n import LANGS, TranslatableMixin
from core.models import Routable, SeoFields, StandardSize, fmt_num
from core.text import is_valid_slug, make_slug


class Technique(TranslatableMixin, models.Model):
    name_ru = models.CharField("Название (RU)", max_length=80)
    name_en = models.CharField("Название (EN)", max_length=80, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Техники"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.name_ru


class Category(TranslatableMixin, SeoFields, Routable):
    parent = models.ForeignKey(
        "self", verbose_name="Родительская рубрика", null=True, blank=True,
        on_delete=models.PROTECT, related_name="children",
    )
    name_ru = models.CharField("Название (RU)", max_length=120)
    name_en = models.CharField("Название (EN)", max_length=120, blank=True, help_text="Пусто — рубрики нет в английской версии.")
    slug_ru = models.CharField("ЧПУ (RU)", max_length=120, blank=True, help_text="Кириллица, например «пейзажи».")
    slug_en = models.CharField("ЧПУ (EN)", max_length=120, blank=True, help_text="Латиница, например «landscapes».")
    intro_ru = models.TextField("Вводный текст (RU)", blank=True)
    intro_en = models.TextField("Вводный текст (EN)", blank=True)
    cover = models.ImageField("Обложка", upload_to="categories/", blank=True)
    cover_alt_ru = models.CharField("Alt обложки (RU)", max_length=200, blank=True)
    cover_alt_en = models.CharField("Alt обложки (EN)", max_length=200, blank=True)
    focus_x = models.PositiveSmallIntegerField("Фокус обложки по горизонтали, %", default=50, validators=[MaxValueValidator(100)])
    focus_y = models.PositiveSmallIntegerField("Фокус обложки по вертикали, %", default=50, validators=[MaxValueValidator(100)])
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики каталога"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return " / ".join(c.name_ru for c in self.ancestors(include_self=True))

    def ancestors(self, include_self=False):
        chain, node, seen = [], (self if include_self else self.parent), set()
        while node is not None and node.pk not in seen:
            seen.add(node.pk)
            chain.append(node)
            node = node.parent
        return list(reversed(chain))

    def descendant_ids(self):
        ids, frontier = [], [self.pk]
        while frontier:
            children = list(Category.objects.filter(parent_id__in=frontier).values_list("pk", flat=True))
            ids.extend(children)
            frontier = children
        return ids

    def clean(self):
        errors = {}
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if slug and not is_valid_slug(slug):
                errors[f"slug_{lang}"] = "Только строчные буквы, цифры и дефисы."
        if errors:
            raise ValidationError(errors)
        if self.parent_id and self.pk:
            if self.parent_id == self.pk or self.parent_id in self.descendant_ids():
                raise ValidationError({"parent": "Рубрику нельзя вложить в саму себя или в ее подрубрику."})
        if not self.slug_ru:
            self.slug_ru = make_slug(self.name_ru, "ru")
        if self.name_en and not self.slug_en:
            self.slug_en = make_slug(self.name_en, "en")
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if slug and Category.objects.filter(parent_id=self.parent_id, **{f"slug_{lang}": slug}).exclude(pk=self.pk).exists():
                raise ValidationError({f"slug_{lang}": "У соседней рубрики уже есть такой адрес."})

    def build_path(self, lang):
        if lang == "en" and not (self.name_en and self.slug_en):
            return ""
        if self.parent_id:
            base = self.parent.path_ru if lang == "ru" else self.parent.path_en
            base = base or ""
        else:
            from content.models import Page

            catalog = Page.objects.filter(kind="catalog").first()
            base = catalog.build_path(lang) if catalog else ""
        slug = getattr(self, f"slug_{lang}")
        return f"{base}{slug}/" if base and slug else ""

    def route_children(self):
        return list(self.children.all())

    def seo_kind(self):
        return "category"

    @property
    def cover_style(self):
        return f"object-position: {self.focus_x}% {self.focus_y}%"

    def is_public(self):
        node = self
        while node is not None:
            if not node.visible:
                return False
            node = node.parent
        return True

    def public_paintings(self, include_sold=None):
        from core.models import SiteSettings

        qs = self.paintings.filter(published=True)
        if include_sold is None:
            include_sold = SiteSettings.get().show_sold_in_catalog
        if not include_sold:
            qs = qs.exclude(status=Painting.SOLD)
        return qs

    def has_content(self):
        """Есть ли опубликованное содержимое в рубрике или ее подрубриках."""
        ids = [self.pk] + self.descendant_ids()
        visible_ids = [c.pk for c in Category.objects.filter(pk__in=ids) if c.is_public()]
        qs = Painting.objects.filter(published=True, category_id__in=visible_ids)
        from core.models import SiteSettings

        if not SiteSettings.get().show_sold_in_catalog:
            qs = qs.exclude(status=Painting.SOLD)
        return qs.exists()


class Painting(TranslatableMixin, SeoFields, Routable):
    AVAILABLE, CUSTOM, SOLD = "available", "custom", "sold"
    STATUSES = [(AVAILABLE, "В наличии"), (CUSTOM, "Под заказ"), (SOLD, "Продана")]
    DESC_TEMPLATE, DESC_OWN = "template", "own"
    SIZES_COMMON, SIZES_OWN = "common", "own"

    title_ru = models.CharField("Название (RU)", max_length=200)
    title_en = models.CharField("Название (EN)", max_length=200, blank=True, help_text="Пусто — картины нет в английской версии.")
    slug_ru = models.CharField("ЧПУ (RU)", max_length=120, blank=True)
    slug_en = models.CharField("ЧПУ (EN)", max_length=120, blank=True)
    sku = models.CharField("Артикул / локальный номер", max_length=40, blank=True)
    category = models.ForeignKey(Category, verbose_name="Рубрика", on_delete=models.PROTECT, related_name="paintings")
    status = models.CharField("Состояние", max_length=12, choices=STATUSES, default=CUSTOM)
    author_ru = models.CharField("Автор (RU)", max_length=120, blank=True)
    author_en = models.CharField("Автор (EN)", max_length=120, blank=True)
    technique = models.ForeignKey(Technique, verbose_name="Техника", null=True, blank=True, on_delete=models.SET_NULL)
    base_ru = models.CharField("Основа (RU)", max_length=120, blank=True, help_text="Например: холст на подрамнике.")
    base_en = models.CharField("Основа (EN)", max_length=120, blank=True)
    framing_ru = models.CharField("Оформление / рама (RU)", max_length=160, blank=True)
    framing_en = models.CharField("Оформление / рама (EN)", max_length=160, blank=True)
    width = models.DecimalField("Фактическая ширина, см", max_digits=6, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    height = models.DecimalField("Фактическая высота, см", max_digits=6, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    year = models.PositiveSmallIntegerField("Год", null=True, blank=True)
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=0, null=True, blank=True,
        help_text="Пусто — показывается «Стоимость по запросу».",
    )
    short_ru = models.CharField("Короткое описание для карточки (RU)", max_length=255, blank=True)
    short_en = models.CharField("Короткое описание для карточки (EN)", max_length=255, blank=True)
    description_mode = models.CharField(
        "Источник описания", max_length=10,
        choices=[(DESC_TEMPLATE, "Общий текст описания"), (DESC_OWN, "Индивидуальное описание")],
        default=DESC_TEMPLATE,
    )
    description_ru = models.TextField("Индивидуальное описание (RU)", blank=True)
    description_en = models.TextField("Индивидуальное описание (EN)", blank=True)
    sizes_mode = models.CharField(
        "Желаемые размеры новой картины", max_length=10,
        choices=[(SIZES_COMMON, "Общий список"), (SIZES_OWN, "Свои размеры")],
        default=SIZES_COMMON,
    )
    published = models.BooleanField("Опубликовано", default=False)
    order = models.IntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Картина"
        verbose_name_plural = "Картины"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title_ru

    def clean(self):
        errors = {}
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if slug and not is_valid_slug(slug):
                errors[f"slug_{lang}"] = "Только строчные буквы, цифры и дефисы."
        if errors:
            raise ValidationError(errors)
        if not self.slug_ru:
            self.slug_ru = make_slug(self.title_ru, "ru")
        if self.title_en and not self.slug_en:
            self.slug_en = make_slug(self.title_en, "en")
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if not slug:
                continue
            if Painting.objects.filter(**{f"slug_{lang}": slug}).exclude(pk=self.pk).exists():
                if self.sku and not slug.endswith(make_slug(self.sku, lang)):
                    setattr(self, f"slug_{lang}", f"{slug}-{make_slug(self.sku, lang)}")
                else:
                    raise ValidationError({f"slug_{lang}": "Картина с таким адресом уже есть. Добавьте артикул или измените ЧПУ."})

    def build_path(self, lang):
        from core.models import SiteSettings

        if lang == "en" and not (self.title_en and self.slug_en):
            return ""
        settings = SiteSettings.get()
        prefix = getattr(settings, f"painting_prefix_{lang}")
        slug = getattr(self, f"slug_{lang}")
        root = "/en/" if lang == "en" else "/"
        return f"{root}{prefix}/{slug}/" if slug else ""

    def seo_kind(self):
        return f"painting_{self.status}"

    @property
    def is_sold(self):
        return self.status == self.SOLD

    @property
    def actual_size(self):
        if self.width and self.height:
            return f"{fmt_num(self.width)} × {fmt_num(self.height)} см"
        return ""

    def main_image(self):
        images = getattr(self, "_prefetched_objects_cache", {}).get("images")
        if images is not None:
            return images[0] if images else None
        return self.images.first()

    def description(self, lang=None):
        """Действующий текст описания: индивидуальный или общий шаблон."""
        from core.i18n import current_lang, tr
        from core.models import SharedBlock

        lang = lang or current_lang()
        if self.description_mode == self.DESC_OWN:
            return tr(self, "description", lang)
        block = SharedBlock.objects.filter(key="painting-description").first()
        return tr(block, "text", lang) if block else ""

    def desired_sizes(self):
        """Список желаемых размеров новой картины (общий или свой)."""
        if self.sizes_mode == self.SIZES_OWN:
            result = []
            for item in self.custom_sizes.select_related("standard"):
                if item.standard_id and not item.standard.visible:
                    continue
                result.append(item.as_option())
            return result
        return [size_option(s) for s in StandardSize.objects.filter(visible=True)]


def size_option(size):
    return {
        "id": f"s{size.pk}",
        "width": size.width,
        "height": size.height,
        "square": size.width == size.height,
        "label": f"{fmt_num(size.width)} × {fmt_num(size.height)}",
    }


class PaintingImage(TranslatableMixin, models.Model):
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Изображение", upload_to="paintings/")
    alt_ru = models.CharField("Alt (RU)", max_length=255, blank=True, help_text="Описание того, что на изображении, без набора ключевых слов.")
    alt_en = models.CharField("Alt (EN)", max_length=255, blank=True)
    caption_ru = models.CharField("Подпись (RU)", max_length=120, blank=True, help_text="Например: деталь, в интерьере.")
    caption_en = models.CharField("Подпись (EN)", max_length=120, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Изображение картины"
        verbose_name_plural = "Изображения (первое — основное)"
        ordering = ["order", "id"]

    def __str__(self):
        return self.image.name


class PaintingSize(models.Model):
    """Индивидуальный список желаемых размеров конкретной картины (раздел 5.2)."""

    painting = models.ForeignKey(Painting, on_delete=models.CASCADE, related_name="custom_sizes")
    standard = models.ForeignKey(
        StandardSize, verbose_name="Стандартный формат", null=True, blank=True, on_delete=models.CASCADE,
    )
    width = models.DecimalField("Ширина, см", max_digits=6, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    height = models.DecimalField("Высота, см", max_digits=6, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(Decimal("0.1"))])
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Свой размер"
        verbose_name_plural = "Свои размеры (при режиме «Свои размеры»)"
        ordering = ["order", "id"]

    def __str__(self):
        if self.standard_id:
            return str(self.standard)
        return f"{fmt_num(self.width)} × {fmt_num(self.height)} см"

    def clean(self):
        if not self.standard_id and not (self.width and self.height):
            raise ValidationError("Выберите стандартный формат или укажите ширину и высоту.")
        if self.standard_id and (self.width or self.height):
            raise ValidationError("Укажите либо стандартный формат, либо свои ширину и высоту.")

    def as_option(self):
        if self.standard_id:
            return size_option(self.standard)
        return {
            "id": f"c{self.pk}",
            "width": self.width,
            "height": self.height,
            "square": self.width == self.height,
            "label": f"{fmt_num(self.width)} × {fmt_num(self.height)}",
        }
