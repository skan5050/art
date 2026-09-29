import hashlib
import hmac
import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone

from leads.models import private_storage


def _hash(secret):
    # Проверочное значение: HMAC с секретом установки; открытый ключ не хранится.
    return hmac.new(settings.SECRET_KEY.encode(), secret.encode(), hashlib.sha256).hexdigest()


class ApiKey(models.Model):
    """Технический ключ импорта. Показывается один раз при выпуске (раздел 11.2)."""

    name = models.CharField("Название подключения", max_length=120)
    prefix = models.CharField("Идентификатор", max_length=16, unique=True, editable=False)
    secret_hash = models.CharField(max_length=64, editable=False)
    can_upload = models.BooleanField("Загрузка фотографий в рубрики", default=True, editable=False)
    can_replace_cover = models.BooleanField("Замена обложки рубрики", default=False)
    can_create_cards = models.BooleanField("Создание карточек-черновиков из фото", default=False)
    can_publish = models.BooleanField("Публикация созданных карточек", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    last_used_at = models.DateTimeField("Последнее использование", null=True, blank=True)
    revoked_at = models.DateTimeField("Отозван", null=True, blank=True)

    class Meta:
        verbose_name = "API-ключ"
        verbose_name_plural = "API импорта — ключи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.prefix})"

    @property
    def is_active(self):
        return self.revoked_at is None

    @classmethod
    def issue(cls, name, **perms):
        """Создает ключ; возвращает (запись, открытый токен). Токен больше не восстановить."""
        prefix = secrets.token_hex(4)
        while cls.objects.filter(prefix=prefix).exists():
            prefix = secrets.token_hex(4)
        secret = secrets.token_urlsafe(32)  # 32 случайных байта из CSPRNG
        key = cls.objects.create(name=name, prefix=prefix, secret_hash=_hash(secret), **perms)
        return key, f"imp_{prefix}_{secret}"

    @classmethod
    def authenticate(cls, token):
        if not token or not token.startswith("imp_"):
            return None
        try:
            _, prefix, secret = token.split("_", 2)
        except ValueError:
            return None
        key = cls.objects.filter(prefix=prefix, revoked_at__isnull=True).first()
        if key is None or not hmac.compare_digest(key.secret_hash, _hash(secret)):
            return None
        cls.objects.filter(pk=key.pk).update(last_used_at=timezone.now())
        return key

    def revoke(self):
        if self.revoked_at is None:
            self.revoked_at = timezone.now()
            self.save(update_fields=["revoked_at"])


def import_path(instance, filename):
    return f"import/{secrets.token_hex(16)}.{filename.rsplit('.', 1)[-1]}"


class ImportRecord(models.Model):
    """Принятый файл импорта. Непубличен, пока администратор не назначит его работе."""

    PURPOSES = [("photo", "Фотография работы"), ("cover", "Обложка рубрики")]
    STATES = [
        ("accepted", "Принят, ждет назначения"),
        ("assigned", "Назначен карточке"),
        ("draft_created", "Создана карточка-черновик"),
        ("published", "Создана и опубликована карточка"),
        ("cover_set", "Установлен как обложка"),
    ]
    api_key = models.ForeignKey(ApiKey, verbose_name="Ключ", null=True, on_delete=models.SET_NULL)
    external_id = models.CharField("Внешний идентификатор", max_length=200)
    category = models.ForeignKey("catalog.Category", verbose_name="Рубрика", null=True, on_delete=models.SET_NULL)
    purpose = models.CharField("Назначение", max_length=10, choices=PURPOSES, default="photo")
    state = models.CharField("Состояние", max_length=20, choices=STATES, default="accepted")
    file = models.FileField("Обработанный файл", storage=private_storage, upload_to=import_path)
    original_name = models.CharField("Имя файла", max_length=255, blank=True)
    sha256 = models.CharField("Контрольная сумма", max_length=64)
    width = models.PositiveIntegerField("Ширина, px", default=0)
    height = models.PositiveIntegerField("Высота, px", default=0)
    painting = models.ForeignKey("catalog.Painting", verbose_name="Картина", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField("Принят", auto_now_add=True)

    class Meta:
        verbose_name = "Файл импорта"
        verbose_name_plural = "API импорта — принятые файлы"
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["external_id"], name="import_unique_external_id")]

    def __str__(self):
        return f"{self.external_id} → {self.category}"


class ImportLog(models.Model):
    """Журнал импорта. Секреты ключей не записываются."""

    created_at = models.DateTimeField("Время", auto_now_add=True, db_index=True)
    key_prefix = models.CharField("Ключ", max_length=16, blank=True)
    action = models.CharField("Действие", max_length=40)
    external_id = models.CharField("Внешний ID", max_length=200, blank=True)
    category_id_value = models.CharField("Рубрика", max_length=40, blank=True)
    file_name = models.CharField("Файл", max_length=255, blank=True)
    result = models.CharField("Результат", max_length=20)
    message = models.CharField("Сообщение", max_length=500, blank=True)

    class Meta:
        verbose_name = "Запись журнала импорта"
        verbose_name_plural = "API импорта — журнал"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%d.%m %H:%M} {self.action} {self.result}"
