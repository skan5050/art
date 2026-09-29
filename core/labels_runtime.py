"""Чтение надписей интерфейса с кешем на время запроса."""
import threading

from .i18n import current_lang
from .labels import DEFAULT_LABELS

_local = threading.local()


def reset():
    _local.labels = None


def _load():
    cached = getattr(_local, "labels", None)
    if cached is None:
        from .models import Label

        cached = {row.key: (row.value_ru, row.value_en) for row in Label.objects.all()}
        _local.labels = cached
    return cached


def label(key, lang=None):
    lang = lang or current_lang()
    row = _load().get(key)
    if row is None:
        default = DEFAULT_LABELS.get(key)
        if default is None:
            return key
        row = (default[1], default[2])
    ru, en = row
    return (en or ru) if lang == "en" else ru
