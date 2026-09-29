from django.db import models

from core.i18n import TranslatableMixin


class City(TranslatableMixin, models.Model):
    """Справочник городов для карты «География наших продаж» (раздел 8.1).

    Импорт справочника не создает продаж: отметка продажи по умолчанию выключена
    и включается владельцем по фактическим данным.
    """

    source = models.CharField("Источник", max_length=40, default="GeoNames")
    source_id = models.CharField("ID в источнике", max_length=40, blank=True, db_index=True)
    country_code = models.CharField("Код страны", max_length=2, db_index=True)
    country_ru = models.CharField("Страна", max_length=80)
    country_en = models.CharField("Страна (EN)", max_length=80, blank=True)
    region = models.CharField("Регион", max_length=120, blank=True)
    name_ru = models.CharField("Название", max_length=120, db_index=True)
    name_en = models.CharField("Название (EN)", max_length=120, blank=True)
    name_source = models.CharField("Название в источнике", max_length=120, blank=True)
    latitude = models.DecimalField("Широта", max_digits=9, decimal_places=5)
    longitude = models.DecimalField("Долгота", max_digits=9, decimal_places=5)
    population = models.PositiveIntegerField("Население", null=True, blank=True)
    population_date = models.CharField("Дата статистики", max_length=40, blank=True)
    is_capital = models.BooleanField("Столица", default=False)
    is_admin_center = models.BooleanField("Административный центр региона", default=False)
    loaded_at = models.DateTimeField("Дата загрузки", null=True, blank=True)
    manually_edited = models.BooleanField(
        "Изменено вручную", default=False, help_text="Обновление справочника не перезаписывает такие записи.",
    )

    sale_confirmed = models.BooleanField("Продажа подтверждена", default=False)
    visible = models.BooleanField("Показывать отметку на карте", default=False)
    caption_ru = models.CharField("Подпись (RU)", max_length=200, blank=True)
    caption_en = models.CharField("Подпись (EN)", max_length=200, blank=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "География продаж — города"
        ordering = ["country_ru", "name_ru"]
        constraints = [
            models.UniqueConstraint(fields=["source", "source_id"], name="city_unique_source",
                                    condition=~models.Q(source_id="")),
        ]

    def __str__(self):
        return f"{self.name_ru} ({self.country_ru})"

    @property
    def on_map(self):
        return self.sale_confirmed and self.visible
