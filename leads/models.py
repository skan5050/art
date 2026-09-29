import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.functional import LazyObject


class PrivateStorage(LazyObject):
    """Хранилище вне публичной медиатеки: веб-сервер его не раздает."""

    def _setup(self):
        from django.conf import settings

        self._wrapped = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT, base_url=None)


private_storage = PrivateStorage()


def attachment_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1].lower()
    return f"leads/{uuid.uuid4().hex}.{ext}"


class Lead(models.Model):
    KINDS = [
        ("general", "Общий заказ"),
        ("category", "Заказ по рубрике"),
        ("painting", "Заказ картины"),
        ("similar", "Заказать похожую"),
        ("custom", "Картина на заказ"),
        ("certificate", "Подарочный сертификат"),
        ("delivery", "Вопрос о доставке"),
        ("question", "Вопрос"),
    ]
    STATUSES = [("new", "Новая"), ("in_progress", "В работе"), ("closed", "Закрыта")]
    CONTACT_METHODS = [
        ("phone", "Телефон"),
        ("telegram", "Telegram"),
        ("whatsapp", "WhatsApp"),
        ("max", "MAX"),
        ("email", "Email"),
    ]
    SIZE_CHOICES = [
        ("", "Не указан"),
        ("standard", "Из списка"),
        ("custom", "Свой размер"),
        ("undecided", "Пока не определился"),
    ]

    status = models.CharField("Статус", max_length=12, choices=STATUSES, default="new", db_index=True)
    kind = models.CharField("Тип обращения", max_length=20, choices=KINDS, default="general")
    painting = models.ForeignKey(
        "catalog.Painting", verbose_name="Картина", null=True, blank=True, on_delete=models.SET_NULL,
    )
    painting_title = models.CharField("Название картины на момент заявки", max_length=200, blank=True)
    painting_status = models.CharField("Состояние картины на момент заявки", max_length=20, blank=True)
    category = models.ForeignKey(
        "catalog.Category", verbose_name="Рубрика", null=True, blank=True, on_delete=models.SET_NULL,
    )
    source_url = models.CharField("Страница, с которой отправлено", max_length=500, blank=True)
    lang = models.CharField("Язык", max_length=2, default="ru")

    name = models.CharField("Имя", max_length=120)
    contact_method = models.CharField("Способ связи", max_length=12, choices=CONTACT_METHODS)
    contact = models.CharField("Контакт", max_length=160)
    city = models.CharField("Город", max_length=120, blank=True)
    deadline = models.CharField("Желаемый срок", max_length=120, blank=True)
    comment = models.TextField("Комментарий", blank=True)

    size_choice = models.CharField("Желаемый размер", max_length=12, choices=SIZE_CHOICES, blank=True)
    size_width = models.DecimalField("Ширина, см", max_digits=6, decimal_places=1, null=True, blank=True)
    size_height = models.DecimalField("Высота, см", max_digits=6, decimal_places=1, null=True, blank=True)
    size_orientation = models.CharField(
        "Расположение", max_length=12, blank=True,
        choices=[("horizontal", "Горизонтальное"), ("vertical", "Вертикальное"), ("square", "Квадрат")],
    )

    certificate_amount = models.PositiveIntegerField("Номинал сертификата", null=True, blank=True)
    certificate_format = models.CharField(
        "Формат сертификата", max_length=12, blank=True,
        choices=[("electronic", "Электронный"), ("print", "Печатный")],
    )

    manager_note = models.TextField("Заметка менеджера", blank=True)
    notification_error = models.CharField("Ошибка уведомления", max_length=255, blank=True)
    idempotency_key = models.CharField(max_length=64, unique=True, null=True, blank=True, editable=False)
    ip_hash = models.CharField(max_length=64, blank=True, editable=False)
    created_at = models.DateTimeField("Получена", auto_now_add=True)
    updated_at = models.DateTimeField("Изменена", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"№{self.pk} · {self.get_kind_display()} · {self.name}"

    @property
    def size_display(self):
        from core.models import fmt_num

        if self.size_choice == "undecided":
            return "Пока не определился"
        if self.size_width and self.size_height:
            extra = f", {self.get_size_orientation_display().lower()}" if self.size_orientation else ""
            source = " (свой)" if self.size_choice == "custom" else ""
            return f"{fmt_num(self.size_width)} × {fmt_num(self.size_height)} см{source}{extra}"
        return ""


class LeadAttachment(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField("Файл", storage=private_storage, upload_to=attachment_path)
    original_name = models.CharField("Имя файла", max_length=200, blank=True)
    size = models.PositiveIntegerField("Размер, байт", default=0)

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.original_name or self.file.name
