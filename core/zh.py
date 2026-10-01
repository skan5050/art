"""Китайская версия сайта: хранилище переводов и вспомогательные функции.

Тексты на китайском хранятся не отдельными колонками, а строками таблицы core.Translation
(объект + поле → текст), поэтому схема существующих моделей и русские/английские страницы не меняются.
Адрес китайской страницы = английский адрес с префиксом /zh/ вместо /en/.
"""
import threading

_local = threading.local()

# Поле заголовка, наличие перевода которого означает «у страницы есть китайская версия».
TITLE_FIELD = {"Page": "title", "Category": "name", "Painting": "title", "Article": "title", "CityLanding": "title"}


def reset():
    _local.cache = None


def target_of(obj):
    return f"{obj._meta.label_lower}:{obj.pk}"


def _cache():
    cache = getattr(_local, "cache", None)
    if cache is None:
        from .models import Translation

        cache = {(row.target, row.field): row.text for row in Translation.objects.filter(lang="zh")}
        _local.cache = cache
    return cache


def zh_get(target, field):
    return _cache().get((target, field), "")


def zh_value(obj, field):
    if obj is None or getattr(obj, "pk", None) is None:
        return ""
    return zh_get(target_of(obj), field)


def zh_has(obj):
    """Есть ли у материала китайская версия (переведен его заголовок)."""
    field = TITLE_FIELD.get(obj.__class__.__name__)
    return bool(field and zh_value(obj, field))


def zh_path_from_en(path_en):
    return "/zh/" + path_en[len("/en/"):] if path_en and path_en.startswith("/en/") else ""


def en_path_from_zh(path):
    return "/en/" + path[len("/zh/"):] if path.startswith("/zh/") else ""
