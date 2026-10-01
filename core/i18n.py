"""Двуязычные поля RU/EN.

Каждое переводимое поле хранится парой колонок: <name>_ru и <name>_en.
Английская версия не переводится автоматически и не подменяется русской:
если EN-значение пустое, его просто нет (раздел 2 дополнения SEO 1.3).
"""
from django.utils import translation

LANGS = ("ru", "en")
DEFAULT_LANG = "ru"
# Китайская версия (/zh/) подключается отдельно: ее тексты хранятся в таблице переводов (core.Translation),
# а адреса повторяют английские. Существующая логика RU/EN, опирающаяся на LANGS, не затрагивается.
ALL_LANGS = ("ru", "en", "zh")
LANG_NAMES = {"ru": "Русский", "en": "English", "zh": "中文"}


def current_lang():
    lang = (translation.get_language() or DEFAULT_LANG)[:2]
    return lang if lang in ALL_LANGS else DEFAULT_LANG


def tr(obj, field, lang=None, fallback=False):
    """Значение переводимого поля для языка (по умолчанию — текущего)."""
    lang = lang or current_lang()
    if lang == "zh":
        from .zh import zh_value

        return zh_value(obj, field)
    value = getattr(obj, f"{field}_{lang}", "") or ""
    if not value and fallback and lang != DEFAULT_LANG:
        value = getattr(obj, f"{field}_{DEFAULT_LANG}", "") or ""
    return value


class TranslatableMixin:
    """Доступ к переводимым полям в шаблонах: {{ obj.t.title }}."""

    @property
    def t(self):
        return _Translated(self)


class _Translated:
    __slots__ = ("_obj",)

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return tr(self._obj, name)

    def __getitem__(self, name):
        return tr(self._obj, name)
