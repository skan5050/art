"""Поиск материала по адресу и проверка конфликтов адресов."""
from django.apps import apps
from django.core.exceptions import ValidationError

ROUTABLE = ("content.Page", "catalog.Category", "catalog.Painting", "content.Article")


def routable_models():
    return [apps.get_model(label) for label in ROUTABLE]


def resolve(path, lang):
    field = f"path_{lang}"
    for model in routable_models():
        obj = model.objects.filter(**{field: path}).first()
        if obj is not None:
            return obj
    return None


def check_conflict(obj, lang):
    path = obj.build_path(lang)
    if not path:
        return
    field = f"path_{lang}"
    for model in routable_models():
        qs = model.objects.filter(**{field: path})
        if isinstance(obj, model) and obj.pk:
            qs = qs.exclude(pk=obj.pk)
        if qs.exists():
            raise ValidationError({f"slug_{lang}": f"Адрес {path} уже занят другим материалом."})


def refresh_all_paths():
    """Пересчет всех адресов (после смены префиксов или массового импорта)."""
    for model in routable_models():
        for obj in model.objects.all():
            obj.refresh_paths()
