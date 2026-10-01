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
        ("cooperation", "Сотрудничество"),
        ("guides", "Полезное (список статей)"),
        ("cities", "Города (список городских страниц)"),
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
    kicker_ru = models.CharField("Надпись над заголовком (RU)", max_length=120, blank=True)
    kicker_en = models.CharField("Надпись над заголовком (EN)", max_length=120, blank=True)
    cta_text_ru = models.CharField("Блок заказа внизу: текст (RU)", max_length=160, blank=True)
    cta_text_en = models.CharField("Блок заказа внизу: текст (EN)", max_length=160, blank=True)
    cta_button_ru = models.CharField("Блок заказа внизу: кнопка (RU)", max_length=80, blank=True)
    cta_button_en = models.CharField("Блок заказа внизу: кнопка (EN)", max_length=80, blank=True)
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
        if self.kind == "cities":
            return list(CityLanding.objects.all())
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


class CityLanding(TranslatableMixin, SeoFields, Routable):
    """Городская страница: ведется вручную, со своим текстом, адресом и картой.

    ТЗ (12.6, SEO-дополнение п. 8): из справочника городов не генерируются однотипные страницы-клоны
    и вымышленные адреса. Поэтому страницы создаются только администратором, текст у каждой свой,
    адрес и координаты заполняются по реальным данным (без адреса карта не показывается).
    """

    city = models.ForeignKey("geo.City", verbose_name="Город из справочника", null=True, blank=True, on_delete=models.SET_NULL,
                             help_text="Связь с картой продаж: в подсказке карты появится ссылка на эту страницу.")
    name_ru = models.CharField("Город (RU)", max_length=80)
    name_en = models.CharField("Город (EN)", max_length=80, blank=True)
    name_in_ru = models.CharField("«в городе» (RU)", max_length=100, blank=True, help_text="Например: «в Москве», «в Казани».")
    title_ru = models.CharField("Заголовок H1 (RU)", max_length=255)
    title_en = models.CharField("Заголовок H1 (EN)", max_length=255, blank=True)
    slug_ru = models.CharField("ЧПУ (RU)", max_length=120, blank=True)
    slug_en = models.CharField("ЧПУ (EN)", max_length=120, blank=True)
    intro_ru = models.TextField("Вступление (RU)", blank=True)
    intro_en = models.TextField("Вступление (EN)", blank=True)
    body_ru = models.TextField("Текст страницы (RU)", blank=True,
                               help_text="Свой текст для этого города. «## Подзаголовок», «- пункт», **жирный**, [ссылка](/адрес/).")
    body_en = models.TextField("Текст страницы (EN)", blank=True)
    delivery_ru = models.TextField("Доставка и получение в городе (RU)", blank=True,
                                   help_text="Как получить картину в этом городе. Только реальные условия.")
    delivery_en = models.TextField("Доставка и получение в городе (EN)", blank=True)
    address_ru = models.CharField("Адрес (RU)", max_length=255, blank=True, help_text="Реальный адрес. Пусто — блок адреса и карта не выводятся.")
    address_en = models.CharField("Адрес (EN)", max_length=255, blank=True)
    address_lat = models.DecimalField("Широта", max_digits=9, decimal_places=6, null=True, blank=True)
    address_lng = models.DecimalField("Долгота", max_digits=9, decimal_places=6, null=True, blank=True)
    hours_ru = models.CharField("Режим работы (RU)", max_length=160, blank=True)
    hours_en = models.CharField("Режим работы (EN)", max_length=160, blank=True)
    phone = models.CharField("Телефон в городе", max_length=40, blank=True, help_text="Пусто — используется общий телефон сайта.")
    cover = models.ImageField("Изображение", upload_to="cities/", blank=True)
    cover_alt_ru = models.CharField("Alt изображения (RU)", max_length=200, blank=True)
    cover_alt_en = models.CharField("Alt изображения (EN)", max_length=200, blank=True)
    button_ru = models.CharField("Кнопка (RU)", max_length=80, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=80, blank=True)
    show_in_picker = models.BooleanField("Показывать в выборе города", default=True,
                                         help_text="Список «Выбрать другой» на городских страницах для посетителей из РФ.")
    geo_aliases = models.TextField("Названия для автоопределения", blank=True,
                                   help_text="Необязательно. По одному на строку: как геобаза может назвать этот город (например, «Yekaterinburg»). "
                                             "Только явные правила, догадок «соседний город ≈ этот» нет.")
    published = models.BooleanField("Опубликовано", default=False)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Городская страница"
        verbose_name_plural = "Города — страницы"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.name_ru

    def clean(self):
        _check_slugs(self)
        if not self.slug_ru:
            self.slug_ru = make_slug(self.name_ru, "ru")
        if self.name_en and not self.slug_en:
            self.slug_en = make_slug(self.name_en, "en")
        for lang in LANGS:
            slug = getattr(self, f"slug_{lang}")
            if slug and CityLanding.objects.filter(**{f"slug_{lang}": slug}).exclude(pk=self.pk).exists():
                raise ValidationError({f"slug_{lang}": "Городская страница с таким адресом уже есть."})
        if (self.address_lat is None) != (self.address_lng is None):
            raise ValidationError({"address_lng": "Укажите обе координаты или оставьте обе пустыми."})

    def save(self, *args, **kwargs):
        if not self.slug_ru:
            self.slug_ru = make_slug(self.name_ru, "ru")
        if self.name_en and not self.slug_en:
            self.slug_en = make_slug(self.name_en, "en")
        super().save(*args, **kwargs)

    def build_path(self, lang):
        if lang == "en" and not (self.title_en and self.slug_en):
            return ""
        parent = Page.objects.filter(kind="cities").first()
        base = parent.build_path(lang) if parent else ""
        slug = getattr(self, f"slug_{lang}")
        return f"{base}{slug}/" if base and slug else ""

    def seo_kind(self):
        return "page"

    @property
    def has_map(self):
        return bool(self.address_ru and self.address_lat is not None and self.address_lng is not None)


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
        if lang == "zh":
            from core.i18n import tr

            label = tr(self, "label", "zh")
            if self.page:
                if not self.page.published or not self.page.url("zh"):
                    return None
                label = label or tr(self.page, "nav_title", "zh") or tr(self.page, "title", "zh")
                href = self.page.url("zh")
            else:
                href = self.url
            return {"label": label, "href": href} if label else None
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
    kicker_ru = models.CharField("Надпись над заголовком (RU)", max_length=120, blank=True)
    kicker_en = models.CharField("Надпись над заголовком (EN)", max_length=120, blank=True)
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
    date = models.DateField("Дата отзыва", null=True, blank=True)
    featured = models.BooleanField("Крупно в начале страницы", default=False)
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


class MediaAsset(TranslatableMixin, models.Model):
    """Медиатека: изображения для вставки в тексты страниц и статей."""

    image = models.ImageField("Изображение", upload_to="library/")
    title = models.CharField("Название в медиатеке", max_length=160)
    alt_ru = models.CharField("Alt (RU)", max_length=255, blank=True)
    alt_en = models.CharField("Alt (EN)", max_length=255, blank=True)
    caption_ru = models.CharField("Подпись (RU)", max_length=255, blank=True)
    caption_en = models.CharField("Подпись (EN)", max_length=255, blank=True)
    uploaded_at = models.DateTimeField("Загружено", auto_now_add=True)

    class Meta:
        verbose_name = "Изображение медиатеки"
        verbose_name_plural = "Медиатека"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    @property
    def snippet(self):
        return f"![{self.alt_ru or self.title}]({self.image.url})" if self.image else ""


# ---------------------------------------------------------------------------
# Страница «Сотрудничество»: все тексты, изображения и преимущества редактируются в админке.
# Сетка, шрифты, палитра, шапка и подвал зафиксированы дизайном A / D и из админки не меняются.
# ---------------------------------------------------------------------------
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator  # noqa: E402

from .coop_icons import ICON_CHOICES, validate_icon_file  # noqa: E402

ACTION_CHOICES = [("form", "Открыть общую форму заявки"), ("url", "Перейти по ссылке")]
_PCT = [MinValueValidator(0), MaxValueValidator(100)]


def _file_or_asset(file, asset):
    if file:
        return file
    if asset is not None and asset.image:
        return asset.image
    return None


class CooperationContent(TranslatableMixin, models.Model):
    """Содержимое страницы «Сотрудничество» (одна запись на сайт): верхний постер, финальный блок и заголовок преимуществ."""

    HERO_MODES = [
        ("brand", "A) Фирменный фон по текущему дизайну"),
        ("split", "B) Фото в правой части, как на эталоне"),
        ("photo_full", "C) Фото на весь фон"),
        ("none", "D) Без изображения"),
    ]

    # --- Верхний постер ---
    hero_mode = models.CharField("Тип фона", max_length=12, choices=HERO_MODES, default="split",
                                 help_text="Если выбран режим с фото, а фото нет или оно скрыто — показывается фирменный фон дизайна. По умолчанию — B, как на эталоне.")
    hero_kicker_ru = models.CharField("Надзаголовок (RU)", max_length=160, blank=True)
    hero_kicker_en = models.CharField("Надзаголовок (EN)", max_length=160, blank=True)
    h1_ru = models.CharField("Заголовок H1 (RU)", max_length=200, blank=True, help_text="Пусто — берётся заголовок страницы.")
    h1_en = models.CharField("Заголовок H1 (EN)", max_length=200, blank=True)
    hero_subtitle_ru = models.CharField("Подзаголовок (RU)", max_length=300, blank=True)
    hero_subtitle_en = models.CharField("Подзаголовок (EN)", max_length=300, blank=True)
    hero_lead_ru = models.TextField("Абзац под подзаголовком (RU)", blank=True)
    hero_lead_en = models.TextField("Абзац под подзаголовком (EN)", blank=True)
    hero_button_ru = models.CharField("Кнопка постера (RU)", max_length=80, blank=True, help_text="Пусто — кнопка не показывается.")
    hero_button_en = models.CharField("Кнопка постера (EN)", max_length=80, blank=True)
    hero_button_action = models.CharField("Действие кнопки постера", max_length=8, choices=ACTION_CHOICES, default="form")
    hero_button_url = models.CharField("Ссылка кнопки постера", max_length=255, blank=True, help_text="Для действия «Перейти по ссылке»: /адрес/ или https://…")
    hero_image = models.ImageField("Фото постера (для компьютера)", upload_to="cooperation/", blank=True)
    hero_image_asset = models.ForeignKey("content.MediaAsset", verbose_name="…или фото из медиатеки", null=True, blank=True,
                                         on_delete=models.SET_NULL, related_name="+")
    hero_image_mobile = models.ImageField("Фото постера для телефона (необязательно)", upload_to="cooperation/", blank=True,
                                          help_text="Нет — используется то же фото с учётом точки фокуса.")
    hero_image_alt_ru = models.CharField("ALT фото (RU)", max_length=255, blank=True)
    hero_image_alt_en = models.CharField("ALT фото (EN)", max_length=255, blank=True)
    hero_show_image = models.BooleanField("Показывать фото постера", default=True, help_text="Снимите галочку, чтобы скрыть фото, не удаляя его.")
    hero_focus_x = models.PositiveSmallIntegerField("Точка фокуса по горизонтали, %", default=50, validators=_PCT)
    hero_focus_y = models.PositiveSmallIntegerField("Точка фокуса по вертикали, %", default=50, validators=_PCT)
    hero_overlay = models.SmallIntegerField("Затемнение (+) / осветление (−) для текста, %", default=35,
                                            validators=[MinValueValidator(-80), MaxValueValidator(80)],
                                            help_text="Только для режима «Фото на весь фон»: от −80 (осветлить) до 80 (затемнить).")

    # --- Финальный блок ---
    cta_title_ru = models.CharField("Финальный блок: заголовок (RU)", max_length=200, blank=True)
    cta_title_en = models.CharField("Финальный блок: заголовок (EN)", max_length=200, blank=True)
    cta_text_ru = models.TextField("Финальный блок: текст (RU)", blank=True)
    cta_text_en = models.TextField("Финальный блок: текст (EN)", blank=True)
    cta_button_ru = models.CharField("Финальный блок: кнопка (RU)", max_length=80, blank=True)
    cta_button_en = models.CharField("Финальный блок: кнопка (EN)", max_length=80, blank=True)
    cta_button_action = models.CharField("Финальный блок: действие кнопки", max_length=8, choices=ACTION_CHOICES, default="form")
    cta_button_url = models.CharField("Финальный блок: ссылка кнопки", max_length=255, blank=True)
    cta_image = models.ImageField("Финальный блок: изображение", upload_to="cooperation/", blank=True)
    cta_image_asset = models.ForeignKey("content.MediaAsset", verbose_name="…или изображение из медиатеки", null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name="+")
    cta_image_alt_ru = models.CharField("Финальный блок: ALT (RU)", max_length=255, blank=True)
    cta_image_alt_en = models.CharField("Финальный блок: ALT (EN)", max_length=255, blank=True)
    cta_show_image = models.BooleanField("Показывать изображение", default=True)
    cta_focus_x = models.PositiveSmallIntegerField("Фокус по горизонтали, %", default=50, validators=_PCT)
    cta_focus_y = models.PositiveSmallIntegerField("Фокус по вертикали, %", default=50, validators=_PCT)

    # --- Преимущества ---
    adv_title_ru = models.CharField("Заголовок блока преимуществ (RU)", max_length=200, blank=True)
    adv_title_en = models.CharField("Заголовок блока преимуществ (EN)", max_length=200, blank=True)

    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        verbose_name = "Страница «Сотрудничество»"
        verbose_name_plural = "Страница «Сотрудничество»"

    def __str__(self):
        return "Страница «Сотрудничество»"

    @classmethod
    def get(cls):
        return cls.objects.order_by("pk").first() or cls.objects.create()

    def _clean_action(self, action, url, field):
        if action == "url":
            url = (url or "").strip()
            if not url or not url.startswith(("/", "http://", "https://", "mailto:", "tel:")):
                raise ValidationError({field: "Укажите адрес: /страница/, https://… , mailto: или tel:."})

    def clean(self):
        self._clean_action(self.hero_button_action, self.hero_button_url, "hero_button_url")
        self._clean_action(self.cta_button_action, self.cta_button_url, "cta_button_url")

    @property
    def hero_file(self):
        return _file_or_asset(self.hero_image, self.hero_image_asset)

    @property
    def cta_file(self):
        return _file_or_asset(self.cta_image, self.cta_image_asset)


class CooperationBlock(TranslatableMixin, models.Model):
    """Один из блоков «текст + фото» страницы «Сотрудничество»."""

    SIDES = [("right", "Фото справа / текст слева"), ("left", "Фото слева / текст справа")]

    content = models.ForeignKey(CooperationContent, on_delete=models.CASCADE, related_name="blocks")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать блок", default=True)
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    image = models.ImageField("Изображение", upload_to="cooperation/", blank=True)
    image_asset = models.ForeignKey("content.MediaAsset", verbose_name="…или из медиатеки", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+")
    alt_ru = models.CharField("ALT (RU)", max_length=255, blank=True)
    alt_en = models.CharField("ALT (EN)", max_length=255, blank=True)
    show_image = models.BooleanField("Показывать изображение", default=True)
    image_side = models.CharField("Положение изображения", max_length=5, choices=SIDES, default="right")
    focus_x = models.PositiveSmallIntegerField("Фокус по горизонтали, %", default=50, validators=_PCT)
    focus_y = models.PositiveSmallIntegerField("Фокус по вертикали, %", default=50, validators=_PCT)

    class Meta:
        verbose_name = "Блок «текст + фото»"
        verbose_name_plural = "Блоки «текст + фото»"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ru or f"Блок {self.pk}"

    @property
    def image_file(self):
        return _file_or_asset(self.image, self.image_asset)


class CooperationAdvantage(TranslatableMixin, models.Model):
    """Преимущество (пиктограмма, название, описание). Каждое редактируется и скрывается отдельно."""

    content = models.ForeignKey(CooperationContent, on_delete=models.CASCADE, related_name="advantages")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)
    icon_key = models.CharField("Пиктограмма из набора", max_length=24, blank=True, choices=ICON_CHOICES,
                                help_text="Пусто — без пиктограммы (пустой рамки не будет).")
    icon_file = models.FileField("…или своя пиктограмма (SVG/PNG)", upload_to="cooperation/icons/", blank=True,
                                 validators=[FileExtensionValidator(["svg", "png", "webp"]), validate_icon_file],
                                 help_text="Загруженный файл заменяет пиктограмму из набора. До 300 КБ.")
    title_ru = models.CharField("Название (RU)", max_length=120, blank=True)
    title_en = models.CharField("Название (EN)", max_length=120, blank=True)
    text_ru = models.CharField("Короткое описание (RU)", max_length=200, blank=True)
    text_en = models.CharField("Короткое описание (EN)", max_length=200, blank=True)

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ru or f"Преимущество {self.pk}"
