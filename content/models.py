from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.i18n import LANGS, TranslatableMixin
from core.models import Routable, SeoFields
from core.text import is_valid_slug, make_slug


def _check_slugs(obj, required_ru=True):
    errors = {}
    for lang in LANGS:
        slug = getattr(obj, f"slug_{lang}")
        if slug and not is_valid_slug(slug):
            errors[f"slug_{lang}"] = "Только строчные буквы, цифры и дефисы, без пробелов."
    if errors:
        raise ValidationError(errors)


class Page(TranslatableMixin, SeoFields, Routable):
    """Основные страницы сайта. Один общий шаблон на тип страницы."""

    KINDS = [
        ("home", "Главная"),
        ("about", "О нас"),
        ("studio", "О студии"),
        ("catalog", "Каталог"),
        ("reviews", "Отзывы"),
        ("delivery", "Доставка"),
        ("contacts", "Контакты"),
        ("sold", "Проданные картины / SOLD"),
        ("certificate", "Подарочный сертификат"),
        ("custom", "Картины на заказ"),
        ("guides", "Полезное (список статей)"),
        ("text", "Текстовая страница"),
    ]
    SINGLE_KINDS = {k for k, _ in KINDS} - {"text"}

    kind = models.CharField("Тип страницы", max_length=20, choices=KINDS, default="text")
    title_ru = models.CharField("Заголовок H1 (RU)", max_length=200)
    title_en = models.CharField("Заголовок H1 (EN)", max_length=200, blank=True, help_text="Пусто — у страницы нет английской версии.")
    nav_title_ru = models.CharField("Короткое название (RU)", max_length=80, blank=True, help_text="Для меню и хлебных крошек.")
    nav_title_en = models.CharField("Короткое название (EN)", max_length=80, blank=True)
    slug_ru = models.CharField("ЧПУ (RU)", max_length=120, blank=True, help_text="Кириллица, например «о-нас». Для главной — пусто.")
    slug_en = models.CharField("ЧПУ (EN)", max_length=120, blank=True, help_text="Латиница, например «about». Адрес будет /en/about/.")
    intro_ru = models.TextField("Вводный текст / анонс (RU)", blank=True)
    intro_en = models.TextField("Вводный текст / анонс (EN)", blank=True)
    body_ru = models.TextField(
        "Основной текст (RU)", blank=True,
        help_text="Абзацы — через пустую строку. «## Подзаголовок», «- пункт», **жирный**, [ссылка](/адрес/), {brand} — название сайта.",
    )
    body_en = models.TextField("Основной текст (EN)", blank=True)
    note_ru = models.TextField("Дополнительный блок (RU)", blank=True, help_text="Выделенный блок условий, подпись под картой и т.п.")
    note_en = models.TextField("Дополнительный блок (EN)", blank=True)
    empty_ru = models.TextField("Текст пустого состояния (RU)", blank=True)
    empty_en = models.TextField("Текст пустого состояния (EN)", blank=True)
    button_ru = models.CharField("Кнопка (RU)", max_length=80, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=80, blank=True)
    image = models.ImageField("Изображение страницы", upload_to="pages/", blank=True)
    image_alt_ru = models.CharField("Alt изображения (RU)", max_length=200, blank=True)
    image_alt_en = models.CharField("Alt изображения (EN)", max_length=200, blank=True)

    # Баннер (используется на главной)
    banner_image = models.ImageField("Баннер: изображение для компьютера", upload_to="banners/", blank=True)
    banner_image_mobile = models.ImageField("Баннер: изображение для телефона", upload_to="banners/", blank=True)
    banner_focus_x = models.PositiveSmallIntegerField("Баннер: фокус по горизонтали, %", default=50)
    banner_focus_y = models.PositiveSmallIntegerField("Баннер: фокус по вертикали, %", default=50)
    banner_kicker_ru = models.CharField("Баннер: надпись над заголовком (RU)", max_length=120, blank=True)
    banner_kicker_en = models.CharField("Баннер: надпись над заголовком (EN)", max_length=120, blank=True)
    banner_title_ru = models.CharField("Баннер: заголовок (RU)", max_length=200, blank=True)
    banner_title_en = models.CharField("Баннер: заголовок (EN)", max_length=200, blank=True)
    banner_text_ru = models.TextField("Баннер: текст (RU)", blank=True)
    banner_text_en = models.TextField("Баннер: текст (EN)", blank=True)
    banner_button1_ru = models.CharField("Баннер: кнопка 1 (RU)", max_length=80, blank=True)
    banner_button1_en = models.CharField("Баннер: кнопка 1 (EN)", max_length=80, blank=True)
    banner_button1_link = models.CharField("Баннер: ссылка кнопки 1", max_length=255, blank=True, help_text="Например, «catalog» — ссылка на каталог; или адрес /…/.")
    banner_button2_ru = models.CharField("Баннер: кнопка 2 (RU)", max_length=80, blank=True, help_text="Открывает форму заказа.")
    banner_button2_en = models.CharField("Баннер: кнопка 2 (EN)", max_length=80, blank=True)

    published = models.BooleanField("Опубликовано", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title_ru} ({self.get_kind_display()})"

    @property
    def nav_title(self):
        return self.t.nav_title or self.t.title

    def clean(self):
        _check_slugs(self)
        if self.kind in self.SINGLE_KINDS:
            clash = Page.objects.filter(kind=self.kind).exclude(pk=self.pk)
            if clash.exists():
                raise ValidationError({"kind": "Страница этого типа уже существует."})
        if self.kind != "home" and not self.slug_ru:
            self.slug_ru = make_slug(self.title_ru, "ru")
        if self.kind != "home" and self.title_en and not self.slug_en:
            self.slug_en = make_slug(self.title_en, "en")
        from core.routing import check_conflict

        for lang in LANGS:
            check_conflict(self, lang)

    def build_path(self, lang):
        if lang == "en" and not self.title_en:
            return ""
        prefix = "/en/" if lang == "en" else "/"
        if self.kind == "home":
            return prefix
        slug = getattr(self, f"slug_{lang}")
        return f"{prefix}{slug}/" if slug else ""

    def route_children(self):
        if self.kind == "catalog":
            from catalog.models import Category

            return list(Category.objects.filter(parent__isnull=True))
        if self.kind == "guides":
            return list(Article.objects.all())
        return []

    def seo_kind(self):
        return "page"


class Article(TranslatableMixin, SeoFields, Routable):
    """Статья раздела «Полезное / Guides» — общий шаблон информационной страницы."""

    title_ru = models.CharField("Заголовок H1 (RU)", max_length=255)
    title_en = models.CharField("Заголовок H1 (EN)", max_length=255, blank=True)
    slug_ru = models.CharField("ЧПУ (RU)", max_length=120, blank=True)
    slug_en = models.CharField("ЧПУ (EN)", max_length=120, blank=True)
    excerpt_ru = models.TextField("Анонс (RU)", blank=True)
    excerpt_en = models.TextField("Анонс (EN)", blank=True)
    body_ru = models.TextField(
        "Текст (RU)", blank=True,
        help_text="Абзацы — через пустую строку. «## Подзаголовок», «- пункт», **жирный**, [ссылка](/адрес/).",
    )
    body_en = models.TextField("Текст (EN)", blank=True)
    button_ru = models.CharField("Кнопка (RU)", max_length=80, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=80, blank=True)
    cover = models.ImageField("Обложка", upload_to="articles/", blank=True)
    cover_alt_ru = models.CharField("Alt обложки (RU)", max_length=200, blank=True)
    cover_alt_en = models.CharField("Alt обложки (EN)", max_length=200, blank=True)
    related_categories = models.ManyToManyField("catalog.Category", verbose_name="Связанные рубрики", blank=True)
    related_paintings = models.ManyToManyField("catalog.Painting", verbose_name="Связанные картины", blank=True)
    published = models.BooleanField("Опубликовано", default=True)
    published_at = models.DateTimeField("Дата публикации", default=timezone.now)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Полезное — статьи"
        ordering = ["order", "-published_at", "id"]

    def __str__(self):
        return self.title_ru

    def clean(self):
        _check_slugs(self)
        if not self.slug_ru:
            self.slug_ru = make_slug(self.title_ru, "ru")
        if self.title_en and not self.slug_en:
            self.slug_en = make_slug(self.title_en, "en")
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if slug and Article.objects.filter(**{f"slug_{lang}": slug}).exclude(pk=self.pk).exists():
                raise ValidationError({f"slug_{lang}": "Статья с таким адресом уже есть."})

    def build_path(self, lang):
        if lang == "en" and not (self.title_en and self.slug_en):
            return ""
        guides = Page.objects.filter(kind="guides").first()
        base = guides.build_path(lang) if guides else ""
        slug = getattr(self, f"slug_{lang}")
        return f"{base}{slug}/" if base and slug else ""

    def seo_kind(self):
        return "article"


class MenuItem(TranslatableMixin, models.Model):
    """Верхнее меню — один список для шапки, мобильного меню и футера."""

    label_ru = models.CharField("Надпись (RU)", max_length=60, blank=True, help_text="Пусто — короткое название выбранной страницы.")
    label_en = models.CharField("Надпись (EN)", max_length=60, blank=True)
    page = models.ForeignKey(Page, verbose_name="Страница", null=True, blank=True, on_delete=models.CASCADE)
    url = models.CharField("Или своя ссылка", max_length=255, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)
    in_footer = models.BooleanField("Повторять в футере", default=True)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню"
        ordering = ["order", "id"]

    def __str__(self):
        return self.label_ru or (self.page.nav_title if self.page else self.url)

    def clean(self):
        if not self.page and not self.url:
            raise ValidationError("Выберите страницу или укажите ссылку.")

    def resolved(self, lang):
        label = getattr(self, f"label_{lang}", "")
        if self.page:
            if not self.page.published:
                return None
            href = self.page.url(lang)
            if not href:
                return None
            label = label or getattr(self.page, f"nav_title_{lang}", "") or getattr(self.page, f"title_{lang}", "")
        else:
            href = self.url
        if not label:
            return None
        return {"label": label, "href": href}


class HomeSection(TranslatableMixin, models.Model):
    """Необязательные блоки главной: включение, заголовки, выбор работ."""

    KINDS = [
        ("intro", "Вводный блок"),
        ("categories", "Рубрики каталога"),
        ("available", "В наличии"),
        ("custom", "Картины под заказ"),
        ("sold", "Проданные работы"),
        ("order", "Индивидуальный заказ"),
        ("reviews", "Отзывы"),
        ("delivery", "Доставка"),
        ("guides", "Полезное"),
    ]
    kind = models.CharField("Блок", max_length=20, choices=KINDS, unique=True)
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    button_ru = models.CharField("Кнопка (RU)", max_length=80, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=80, blank=True)
    image = models.ImageField("Изображение блока", upload_to="home/", blank=True)
    paintings = models.ManyToManyField(
        "catalog.Painting", verbose_name="Работы для показа", blank=True,
        help_text="Пусто — последние опубликованные работы с подходящим статусом.",
    )
    limit = models.PositiveSmallIntegerField("Сколько работ показывать", default=4)
    visible = models.BooleanField("Показывать", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Блок главной"
        verbose_name_plural = "Главная — блоки"
        ordering = ["order", "id"]

    def __str__(self):
        return self.get_kind_display()


class Review(TranslatableMixin, models.Model):
    text_ru = models.TextField("Текст отзыва (RU)")
    text_en = models.TextField("Текст отзыва (EN)", blank=True)
    author_ru = models.CharField("Имя или подпись (RU)", max_length=120)
    author_en = models.CharField("Имя или подпись (EN)", max_length=120, blank=True)
    city_ru = models.CharField("Город (RU)", max_length=80, blank=True)
    city_en = models.CharField("Город (EN)", max_length=80, blank=True)
    photo = models.ImageField("Фото", upload_to="reviews/", blank=True)
    painting = models.ForeignKey("catalog.Painting", verbose_name="Картина", null=True, blank=True, on_delete=models.SET_NULL)
    published = models.BooleanField("Опубликован", default=False)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.author_ru}: {self.text_ru[:50]}"


class CertificateNominal(TranslatableMixin, models.Model):
    amount = models.PositiveIntegerField("Номинал")
    label_ru = models.CharField("Подпись (RU)", max_length=80, blank=True)
    label_en = models.CharField("Подпись (EN)", max_length=80, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Номинал сертификата"
        verbose_name_plural = "Номиналы сертификата"
        ordering = ["order", "amount"]

    def __str__(self):
        return f"{self.amount:,}".replace(",", " ")


class StudioImage(TranslatableMixin, models.Model):
    """Изображения раздела о студии (свои на каждом сайте)."""

    image = models.ImageField("Изображение", upload_to="studio/")
    alt_ru = models.CharField("Alt (RU)", max_length=200, blank=True)
    alt_en = models.CharField("Alt (EN)", max_length=200, blank=True)
    caption_ru = models.CharField("Подпись (RU)", max_length=200, blank=True)
    caption_en = models.CharField("Подпись (EN)", max_length=200, blank=True)
    is_illustration = models.BooleanField(
        "Иллюстрация, а не фотография реального помещения", default=True,
        help_text="Для сгенерированных изображений: рядом выводится нейтральная пометка, что это иллюстрация.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Изображение студии"
        verbose_name_plural = "О студии — изображения"
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption_ru or self.image.name
