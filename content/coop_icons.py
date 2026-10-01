"""Набор пиктограмм страницы «Сотрудничество»: линейные SVG на currentColor — цвет задаёт дизайн A или D."""
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

ICONS = {
    "individual": "Человек — индивидуальный подход",
    "flexible": "Палитра — гибкие решения",
    "brief": "Планшет с отметкой — работа по ТЗ",
    "delivery": "Грузовик — доставка",
    "longterm": "Сердце — долгосрочное сотрудничество",
    "frame": "Рамка с картиной",
    "ruler": "Линейка — размеры",
    "chat": "Диалог — обсуждение",
    "clock": "Часы — сроки",
    "shield": "Щит с галочкой — надёжность",
    "globe": "Глобус — география",
    "package": "Коробка — упаковка",
}
ICON_CHOICES = list(ICONS.items())
MAX_ICON_BYTES = 300 * 1024
_BAD_SVG = (b"<script", b"javascript:", b"onload", b"onerror", b"<foreignobject", b"<iframe", b"<!entity")


def _dir():
    return Path(settings.BASE_DIR) / "static" / "common" / "img" / "coop"


@lru_cache(maxsize=None)
def _svg(key):
    path = _dir() / f"{key}.svg"
    return path.read_text(encoding="utf-8") if key in ICONS and path.exists() else ""


def inline_svg(key):
    """Встроенный SVG выбранной пиктограммы (пусто, если ключа нет)."""
    svg = _svg(key)
    return mark_safe(svg.replace("<svg ", '<svg class="coop-icon-svg" aria-hidden="true" focusable="false" ', 1)) if svg else ""


def validate_icon_file(f):
    if f.size > MAX_ICON_BYTES:
        raise ValidationError("Файл больше 300 КБ.")
    if f.name.lower().endswith(".svg"):
        head = f.read(MAX_ICON_BYTES + 1).lower()
        f.seek(0)
        if b"<svg" not in head or any(bad in head for bad in _BAD_SVG):
            raise ValidationError("SVG должен быть простым рисунком без скриптов и внешних объектов.")
