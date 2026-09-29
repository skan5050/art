from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction

from .i18n import LANGS, TranslatableMixin, tr
from .text import is_valid_slug

ROBOTS_DEFAULT = """User-agent: *
Disallow: /{admin_path}
Disallow: /api/v1/import/
Disallow: /lead/

Sitemap: {site_url}/sitemap.xml
"""


class SiteSettings(TranslatableMixin, models.Model):
    """«Общие настройки» — единственная запись на установку сайта."""

    # Бренд
    brand_name_ru = models.CharField("Название (RU)", max_length=80, default="МираМе")
    brand_name_en = models.CharField("Название (EN)", max_length=80, blank=True)
    slogan_ru = models.CharField("Слоган (RU)", max_length=160, blank=True)
    slogan_en = models.CharField("Слоган (EN)", max_length=160, blank=True)
    logo = models.ImageField("Логотип", upload_to="brand/", blank=True)
    logo_on_dark = models.ImageField("Логотип для темного фона", upload_to="brand/", blank=True)
    logo_alt_ru = models.CharField("Альтернативный текст логотипа (RU)", max_length=160, blank=True)
    logo_alt_en = models.CharField("Альтернативный текст логотипа (EN)", max_length=160, blank=True)
    favicon = models.ImageField("Favicon", upload_to="brand/", blank=True, help_text="Квадратное PNG-изображение от 192×192 px.")
    logo_contains_slogan = models.BooleanField(
        "Слоган уже есть внутри файла логотипа", default=True,
        help_text="Тогда слоган не дублируется отдельной надписью рядом с логотипом.",
    )

    header_note_ru = models.CharField("Подпись в шапке (RU)", max_length=120, blank=True, help_text="Короткая строка справа в шапке внутренних страниц.")
    header_note_en = models.CharField("Подпись в шапке (EN)", max_length=120, blank=True)

    # Адрес сайта
    base_url = models.URLField(
        "Основной адрес сайта", blank=True,
        help_text="Например, https://mirame.ru — без слеша в конце. Используется в canonical, sitemap, robots.txt, hreflang, Open Graph и разметке.",
    )

    # Контакты
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    address_ru = models.CharField(
        "Адрес (RU)", max_length=255, blank=True,
        help_text="Заполняйте только при реальной точке приема клиентов. Личного приема нет — оставьте пустым.",
    )
    address_en = models.CharField("Адрес (EN)", max_length=255, blank=True)
    hours_ru = models.CharField("Режим ответа (RU)", max_length=160, blank=True)
    hours_en = models.CharField("Режим ответа (EN)", max_length=160, blank=True)
    geography_ru = models.CharField("География работы (RU)", max_length=255, blank=True)
    geography_en = models.CharField("География работы (EN)", max_length=255, blank=True)

    # Футер
    copyright_ru = models.CharField("Копирайт (RU)", max_length=160, blank=True, default="© {year} {brand}")
    copyright_en = models.CharField("Копирайт (EN)", max_length=160, blank=True, default="© {year} {brand}")

    # Каталог
    show_sold_in_catalog = models.BooleanField(
        "Показывать проданные в рубриках каталога", default=True,
        help_text="Если выключено, проданные работы видны только в разделе SOLD.",
    )
    painting_prefix_ru = models.CharField("Префикс адреса картины (RU)", max_length=40, default="картина")
    painting_prefix_en = models.CharField("Префикс адреса картины (EN)", max_length=40, default="painting")
    per_page = models.PositiveSmallIntegerField("Картин на странице списка", default=24, validators=[MinValueValidator(4)])
    currency = models.CharField("Валюта цен", max_length=8, default="₽")

    # Сертификат
    certificate_image = models.ImageField("Изображение сертификата", upload_to="certificate/", blank=True)
    certificate_custom_amount = models.BooleanField("Разрешить произвольную сумму сертификата", default=False)
    certificate_electronic = models.BooleanField("Доступен электронный сертификат", default=False)
    certificate_print = models.BooleanField("Доступен печатный сертификат", default=False)

    # Карта продаж
    map_tiles_url = models.CharField(
        "Адрес тайлов карты", max_length=255, default="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    )
    map_attribution = models.CharField(
        "Подпись источника карты", max_length=255,
        default='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    )

    # Формы
    consent_checkbox = models.BooleanField(
        "Галочка согласия в формах", default=True,
        help_text="Отправка возможна только с отметкой согласия. Текст — надпись form.consent; ссылка — страница, указанная ниже.",
    )
    privacy_page_url = models.CharField("Ссылка на политику обработки данных", max_length=255, blank=True)

    # Уведомления
    notify_emails = models.CharField(
        "Email для уведомлений о заявках", max_length=500, blank=True, help_text="Несколько адресов — через запятую.",
    )

    # SEO и сервисы
    robots_txt = models.TextField("robots.txt", default=ROBOTS_DEFAULT)
    robots_disallow_all_confirmed = models.BooleanField(
        "Подтверждаю закрытие всего сайта от индексации", default=False,
        help_text="Нужно только если в robots.txt есть «Disallow: /». Для рабочего сайта не используется.",
    )
    yandex_verification = models.CharField("Код Яндекс Вебмастера", max_length=80, blank=True)
    google_verification = models.CharField("Код Google Search Console", max_length=120, blank=True)
    yandex_metrika_id = models.CharField("Номер счетчика Яндекс Метрики", max_length=20, blank=True)
    ga4_id = models.CharField("Идентификатор GA4", max_length=20, blank=True, help_text="Вида G-XXXXXXX")
    analytics_enabled = models.BooleanField("Включить счетчики", default=False)
    sitemap_generated_at = models.DateTimeField("Последняя генерация sitemap.xml", null=True, blank=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Общие настройки"
        verbose_name_plural = "Общие настройки"

    def __str__(self):
        return "Общие настройки сайта"

    @classmethod
    def get(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        self.base_url = (self.base_url or "").rstrip("/")
        super().save(*args, **kwargs)

    def clean(self):
        import re

        if self.yandex_verification and not re.fullmatch(r"[A-Za-z0-9_-]+", self.yandex_verification):
            raise ValidationError({"yandex_verification": "Укажите только код из content=\"…\", без HTML."})
        if self.google_verification and not re.fullmatch(r"[A-Za-z0-9_-]+", self.google_verification):
            raise ValidationError({"google_verification": "Укажите только код из content=\"…\", без HTML."})
        if self.yandex_metrika_id and not self.yandex_metrika_id.isdigit():
            raise ValidationError({"yandex_metrika_id": "Номер счетчика состоит из цифр."})
        if self.ga4_id and not re.fullmatch(r"G-[A-Z0-9]+", self.ga4_id):
            raise ValidationError({"ga4_id": "Формат: G-XXXXXXX."})
        if robots_disallows_all(self.robots_txt) and not self.robots_disallow_all_confirmed:
            raise ValidationError({"robots_txt": "В robots.txt закрыт весь сайт (Disallow: /). Подтвердите это отдельной галочкой ниже."})
        for lang in LANGS:
            prefix = getattr(self, f"painting_prefix_{lang}")
            if not is_valid_slug(prefix):
                raise ValidationError({f"painting_prefix_{lang}": "Строчные буквы, цифры и дефисы."})

    def brand(self, lang=None):
        return tr(self, "brand_name", lang, fallback=True)

    def absolute(self, path, request=None):
        from django.utils.encoding import iri_to_uri

        base = self.base_url
        if not base and request is not None:
            base = f"{request.scheme}://{request.get_host()}"
        return iri_to_uri(f"{base}{path}")

    def rendered_robots(self, request=None):
        from django.conf import settings

        base = self.base_url
        if not base and request is not None:
            base = f"{request.scheme}://{request.get_host()}"
        return self.robots_txt.replace("{site_url}", base).replace("{admin_path}", settings.ADMIN_PATH)


def robots_disallows_all(text):
    agent_all = False
    for raw in (text or "").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            agent_all = value == "*"
        elif key == "disallow" and agent_all and value == "/":
            return True
    return False


class SeoTemplate(models.Model):
    """Шаблоны Title/Description по типам материалов (приложение Д5)."""

    KINDS = [
        ("painting_available", "Картина — в наличии"),
        ("painting_custom", "Картина — под заказ"),
        ("painting_sold", "Картина — продана"),
        ("category", "Рубрика"),
        ("article", "Статья"),
        ("page", "Страница"),
        ("list_page", "Страница списка N > 1"),
    ]
    kind = models.CharField("Тип", max_length=40, choices=KINDS, unique=True)
    title_ru = models.CharField("Title (RU), после «{brand} |»", max_length=200, blank=True)
    title_en = models.CharField("Title (EN), после «{brand} |»", max_length=200, blank=True)
    description_ru = models.TextField("Description (RU)", blank=True)
    description_en = models.TextField("Description (EN)", blank=True)

    class Meta:
        verbose_name = "SEO-шаблон"
        verbose_name_plural = "SEO-шаблоны по типам страниц"
        ordering = ["kind"]

    def __str__(self):
        return self.get_kind_display()


class Label(TranslatableMixin, models.Model):
    """Надписи интерфейса: кнопки, поля форм, статусы, ошибки (RU/EN)."""

    key = models.CharField("Ключ", max_length=80, unique=True)
    group = models.CharField("Группа", max_length=40, blank=True)
    hint = models.CharField("Где используется", max_length=255, blank=True)
    value_ru = models.TextField("Текст (RU)")
    value_en = models.TextField("Текст (EN)", blank=True)

    class Meta:
        verbose_name = "Надпись интерфейса"
        verbose_name_plural = "Надписи интерфейса"
        ordering = ["group", "key"]

    def __str__(self):
        return f"{self.key}: {self.value_ru[:60]}"


class SharedBlock(TranslatableMixin, models.Model):
    """Сквозной текстовый блок: один источник для всех мест использования."""

    key = models.SlugField("Ключ", max_length=60, unique=True)
    name = models.CharField("Название в админке", max_length=120)
    usage = models.CharField("Где используется", max_length=255, blank=True)
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    title_en = models.CharField("Заголовок (EN)", max_length=200, blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)
    text_en = models.TextField("Текст (EN)", blank=True)
    button_ru = models.CharField("Кнопка (RU)", max_length=80, blank=True)
    button_en = models.CharField("Кнопка (EN)", max_length=80, blank=True)
    visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Сквозной блок"
        verbose_name_plural = "Сквозные блоки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Messenger(models.Model):
    ICONS = [
        ("telegram", "Telegram"),
        ("whatsapp", "WhatsApp"),
        ("max", "MAX"),
        ("vk", "VK"),
        ("viber", "Viber"),
        ("email", "Email"),
        ("phone", "Телефон"),
    ]
    name = models.CharField("Название", max_length=40)
    icon = models.CharField("Значок", max_length=20, choices=ICONS)
    url = models.CharField("Ссылка", max_length=255, help_text="https://t.me/…, https://wa.me/…, mailto:…, tel:…")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры и каналы связи"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    def clean(self):
        if not self.url.startswith(("https://", "http://", "mailto:", "tel:")):
            raise ValidationError({"url": "Ссылка должна начинаться с https://, mailto: или tel:"})


class StandardSize(models.Model):
    """«Общие настройки → Размеры картин» — один справочник на сайт (раздел 5.1)."""

    GROUPS = [("rect", "Прямоугольные"), ("square", "Квадратные"), ("pano", "Панорамные")]
    width = models.DecimalField("Меньшая сторона, см", max_digits=6, decimal_places=1, validators=[MinValueValidator(1)])
    height = models.DecimalField("Большая сторона, см", max_digits=6, decimal_places=1, validators=[MinValueValidator(1)])
    group = models.CharField("Группа", max_length=10, choices=GROUPS, default="rect")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Стандартный размер"
        verbose_name_plural = "Размеры картин (общий список)"
        ordering = ["order", "width", "height"]

    def __str__(self):
        return f"{fmt_num(self.width)} × {fmt_num(self.height)} см"

    @property
    def is_square(self):
        return self.width == self.height

    def clean(self):
        if self.width and self.height and self.width > self.height:
            self.width, self.height = self.height, self.width


def fmt_num(value):
    if value is None:
        return ""
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return text.replace(".", ",")


class Redirect(models.Model):
    """Постоянные перенаправления со старых адресов (создаются автоматически)."""

    old_path = models.CharField("Старый адрес", max_length=500, unique=True)
    new_path = models.CharField("Новый адрес", max_length=500)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Перенаправление 301"
        verbose_name_plural = "Перенаправления 301"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.old_path} → {self.new_path}"

    @classmethod
    def register(cls, old, new):
        if not old or old == new:
            return
        with transaction.atomic():
            # Без цепочек: все старые адреса ведут сразу на актуальный.
            cls.objects.filter(new_path=old).update(new_path=new)
            cls.objects.update_or_create(old_path=old, defaults={"new_path": new})
            cls.objects.filter(old_path=new).delete()
            cls.objects.filter(old_path=models.F("new_path")).delete()


class Routable(models.Model):
    """Материал с собственным адресом в RU и EN версиях.

    Адрес вычисляется из ЧПУ и родителей и хранится для быстрого поиска.
    При изменении адреса опубликованного материала создается 301-редирект
    со старого адреса, включая вложенные материалы.
    """

    path_ru = models.CharField("Адрес RU", max_length=500, blank=True, db_index=True, editable=False)
    path_en = models.CharField("Адрес EN", max_length=500, blank=True, db_index=True, editable=False)

    class Meta:
        abstract = True

    def build_path(self, lang):
        raise NotImplementedError

    def route_children(self):
        return []

    def has_lang(self, lang):
        return bool(getattr(self, f"path_{lang}", ""))

    def url(self, lang=None):
        from .i18n import current_lang

        return getattr(self, f"path_{lang or current_lang()}", "") or ""

    def get_absolute_url(self):
        return self.url()

    def refresh_paths(self):
        changed = {}
        for lang in LANGS:
            old = getattr(self, f"path_{lang}")
            new = self.build_path(lang) or ""
            if old != new:
                changed[f"path_{lang}"] = new
                if old and new:
                    Redirect.register(old, new)
                setattr(self, f"path_{lang}", new)
        if changed:
            type(self).objects.filter(pk=self.pk).update(**changed)
        for child in self.route_children():
            child.refresh_paths()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_paths()


class SeoFields(models.Model):
    """Вкладка «SEO» материала (раздел 11.3 ТЗ, раздел 7 дополнения)."""

    seo_title_ru = models.CharField(
        "SEO Title (RU)", max_length=200, blank=True,
        help_text="Смысловая часть после «Бренд |». Пусто — значение по шаблону типа страницы.",
    )
    seo_title_en = models.CharField("SEO Title (EN)", max_length=200, blank=True)
    seo_description_ru = models.TextField("Description (RU)", blank=True, help_text="Поддерживается вставка {brand}.")
    seo_description_en = models.TextField("Description (EN)", blank=True)
    og_title_ru = models.CharField("Open Graph: заголовок (RU)", max_length=200, blank=True)
    og_title_en = models.CharField("Open Graph: заголовок (EN)", max_length=200, blank=True)
    og_description_ru = models.CharField("Open Graph: описание (RU)", max_length=300, blank=True)
    og_description_en = models.CharField("Open Graph: описание (EN)", max_length=300, blank=True)
    og_image = models.ImageField("Open Graph: изображение", upload_to="og/", blank=True)
    indexable = models.BooleanField(
        "Показывать в поиске", default=True,
        help_text="Если выключено — noindex и исключение из sitemap.xml.",
    )
    canonical_override = models.CharField(
        "Canonical вручную", max_length=500, blank=True,
        help_text="Обычно пусто: canonical формируется автоматически. Указывайте адрес основной версии только для дублей, например /каталог/море/.",
    )

    class Meta:
        abstract = True
