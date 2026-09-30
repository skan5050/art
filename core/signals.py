from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Label, Redirect, SiteSettings


def _drop_redirects(sender, instance, **kwargs):
    # Удаленная без замены страница должна отвечать 404, а не перенаправлять на пустоту.
    paths = [p for p in (getattr(instance, "path_ru", ""), getattr(instance, "path_en", "")) if p]
    if paths:
        Redirect.objects.filter(new_path__in=paths).delete()


def _indexnow_deleted(sender, instance, **kwargs):
    from . import indexnow

    indexnow.notify([p for p in (getattr(instance, "path_ru", ""), getattr(instance, "path_en", "")) if p])


def connect_routables():
    from .routing import routable_models

    for model in routable_models():
        post_delete.connect(_drop_redirects, sender=model, dispatch_uid=f"drop-redirects-{model.__name__}")
        post_delete.connect(_indexnow_deleted, sender=model, dispatch_uid=f"indexnow-delete-{model.__name__}")


@receiver(pre_save, sender=SiteSettings)
def _remember_prefixes(sender, instance, **kwargs):
    old = SiteSettings.objects.filter(pk=1).values("painting_prefix_ru", "painting_prefix_en").first()
    instance._old_prefixes = old


@receiver(post_save, sender=SiteSettings)
def _refresh_painting_paths(sender, instance, **kwargs):
    old = getattr(instance, "_old_prefixes", None)
    if old and (old["painting_prefix_ru"] != instance.painting_prefix_ru or old["painting_prefix_en"] != instance.painting_prefix_en):
        from catalog.models import Painting

        for painting in Painting.objects.all():
            painting.refresh_paths()


@receiver(post_save, sender=Label)
def _reset_labels(sender, **kwargs):
    from . import labels_runtime

    labels_runtime.reset()


connect_routables()
