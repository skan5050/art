from django.core.files.base import ContentFile

from catalog.models import Painting, PaintingImage


def create_card_from_record(record, publish=False, title=None):
    """Карточка из принятого файла: общий текст описания, общий список размеров.

    Цена, фактический размер, техника и статус «В наличии»/«Продана» не назначаются.
    """
    base_title = title or record.original_name.rsplit(".", 1)[0] or record.external_id
    painting = Painting(
        title_ru=base_title[:200], sku=record.external_id[:40], category=record.category,
        status=Painting.CUSTOM, published=publish,
    )
    painting.full_clean(exclude=["slug_en", "title_en"])
    painting.save()
    record.file.open("rb")
    try:
        data = record.file.read()
    finally:
        record.file.close()
    ext = record.file.name.rsplit(".", 1)[-1]
    image = PaintingImage(painting=painting, order=0)
    image.image.save(f"{painting.pk}-{record.pk}.{ext}", ContentFile(data), save=True)
    record.painting = painting
    record.state = "published" if publish else "draft_created"
    record.save(update_fields=["painting", "state"])
    return painting


def assign_record_to_painting(record, painting):
    record.file.open("rb")
    try:
        data = record.file.read()
    finally:
        record.file.close()
    ext = record.file.name.rsplit(".", 1)[-1]
    order = painting.images.count()
    image = PaintingImage(painting=painting, order=order)
    image.image.save(f"{painting.pk}-{record.pk}.{ext}", ContentFile(data), save=True)
    record.painting = painting
    record.state = "assigned"
    record.save(update_fields=["painting", "state"])
    return image
