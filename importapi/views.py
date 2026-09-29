"""API импорта фотографий по рубрикам (раздел 11.1 ТЗ).

GET  /api/v1/import/categories            — дерево рубрик с постоянными ID
POST /api/v1/import/images                — файл + external_id + category_id + purpose
GET  /api/v1/import/results/<external_id> — результат по внешнему ID (для повтора после обрыва)
"""
import hashlib
import io
from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageOps

from catalog.models import Category

from .models import ApiKey, ImportLog, ImportRecord

FORMATS = {"JPEG": ("jpg", "JPEG"), "PNG": ("png", "PNG"), "WEBP": ("webp", "WEBP")}


def _error(status, code, message, **extra):
    return JsonResponse({"ok": False, "error": code, "message": message, **extra}, status=status)


def _log(key, action, result, message="", external_id="", category="", file_name=""):
    ImportLog.objects.create(
        key_prefix=key.prefix if key else "", action=action, result=result, message=message[:500],
        external_id=external_id[:200], category_id_value=str(category)[:40], file_name=file_name[:255],
    )


def api_auth(view):
    @csrf_exempt
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.is_secure() and not settings.DEBUG:
            return _error(403, "https_required", "Используйте HTTPS.")
        header = request.headers.get("Authorization", "")
        token = header[7:].strip() if header.lower().startswith("bearer ") else ""
        key = ApiKey.authenticate(token)
        if key is None:
            _log(None, view.__name__, "denied", "Неверный или отозванный ключ")
            return _error(401, "unauthorized", "Ключ не принят: неверный или отозван.")
        window = timezone.now() - timedelta(minutes=1)
        if ImportLog.objects.filter(key_prefix=key.prefix, created_at__gte=window).count() >= settings.IMPORT_RATE_PER_MINUTE:
            return _error(429, "rate_limited", "Слишком много запросов. Повторите через минуту.")
        request.api_key = key
        return view(request, *args, **kwargs)

    return wrapper


def _category_tree():
    nodes = {}
    for cat in Category.objects.all().order_by("order", "name_ru"):
        nodes[cat.pk] = {
            "id": cat.pk, "parent_id": cat.parent_id, "name": cat.name_ru, "name_en": cat.name_en,
            "path": " / ".join(c.name_ru for c in cat.ancestors(include_self=True)), "visible": cat.visible,
        }
    return sorted(nodes.values(), key=lambda n: n["path"])


@api_auth
def categories(request):
    if request.method != "GET":
        return _error(405, "method_not_allowed", "Только GET.")
    _log(request.api_key, "categories", "ok")
    return JsonResponse({"ok": True, "categories": _category_tree()})


def _record_payload(record, duplicate=False):
    return {
        "ok": True,
        "duplicate": duplicate,
        "external_id": record.external_id,
        "record_id": record.pk,
        "category_id": record.category_id,
        "purpose": record.purpose,
        "state": record.state,
        "state_display": record.get_state_display(),
        "painting_id": record.painting_id,
        "width": record.width,
        "height": record.height,
    }


@api_auth
def result(request, external_id):
    if request.method != "GET":
        return _error(405, "method_not_allowed", "Только GET.")
    record = ImportRecord.objects.filter(external_id=external_id).first()
    if record is None:
        return _error(404, "not_found", "Файл с таким внешним ID не принимался.")
    return JsonResponse(_record_payload(record))


def process_image(raw):
    """Проверка реального формата, декодирование и пересохранение без изменения картины."""
    Image.MAX_IMAGE_PIXELS = settings.IMPORT_MAX_PIXELS
    try:
        with Image.open(io.BytesIO(raw)) as probe:
            fmt = probe.format
            probe.verify()
        if fmt not in FORMATS:
            return None, "unsupported_format"
        with Image.open(io.BytesIO(raw)) as img:
            if img.width * img.height > settings.IMPORT_MAX_PIXELS:
                return None, "too_many_pixels"
            img.load()
            icc = img.info.get("icc_profile")
            img = ImageOps.exif_transpose(img)
            ext, save_fmt = FORMATS[fmt]
            if save_fmt == "JPEG" and img.mode not in ("RGB", "L", "CMYK"):
                img = img.convert("RGB")
            out = io.BytesIO()
            params = {"icc_profile": icc} if icc else {}
            if save_fmt == "JPEG":
                params.update(quality=95, subsampling=0)
            elif save_fmt == "WEBP":
                params.update(quality=95)
            img.save(out, save_fmt, **params)  # метаданные EXIF не переносятся, профиль цвета сохраняется
            return (out.getvalue(), ext, img.width, img.height), None
    except Image.DecompressionBombError:
        return None, "too_many_pixels"
    except Exception:  # noqa: BLE001
        return None, "unsupported_format"


ERRORS = {
    "unsupported_format": "Допустимы только JPG, PNG, WEBP; файл не распознан как изображение.",
    "too_many_pixels": "Слишком большое разрешение изображения.",
}


@api_auth
def upload_image(request):
    key = request.api_key
    if request.method != "POST":
        return _error(405, "method_not_allowed", "Только POST.")
    external_id = (request.POST.get("external_id") or "").strip()
    category_raw = (request.POST.get("category_id") or "").strip()
    purpose = (request.POST.get("purpose") or "photo").strip()
    upload = request.FILES.get("file")
    name = upload.name if upload else ""

    def fail(status, code, message):
        _log(key, "upload", "rejected", f"{code}: {message}", external_id, category_raw, name)
        return _error(status, code, message)

    if not external_id or len(external_id) > 200:
        return fail(400, "external_id_required", "Укажите external_id (до 200 символов).")
    if purpose not in ("photo", "cover"):
        return fail(400, "bad_purpose", "purpose: photo или cover.")
    if purpose == "cover" and not key.can_replace_cover:
        return fail(403, "forbidden", "Ключу не разрешена замена обложек.")
    if not category_raw.isdigit():
        return fail(400, "category_required", "Укажите числовой category_id.")
    category = Category.objects.filter(pk=int(category_raw)).first()
    if category is None:
        return fail(404, "category_not_found", "Рубрика не найдена. Похожая не подбирается и новая не создается.")
    if upload is None:
        return fail(400, "file_required", "Передайте файл в поле file.")
    if upload.size > settings.IMPORT_MAX_FILE_MB * 1024 * 1024:
        return fail(413, "file_too_large", f"Файл больше {settings.IMPORT_MAX_FILE_MB} МБ.")

    raw = upload.read()
    digest = hashlib.sha256(raw).hexdigest()

    existing = ImportRecord.objects.filter(external_id=external_id).first()
    if existing:
        if existing.sha256 == digest and existing.category_id == category.pk and existing.purpose == purpose:
            _log(key, "upload", "duplicate", "Повтор уже принятого файла", external_id, category.pk, name)
            return JsonResponse(_record_payload(existing, duplicate=True))
        return fail(409, "conflict", "Этот external_id уже занят другим файлом; обновление без отдельного права не выполняется.")

    processed, error = process_image(raw)
    if error:
        return fail(415 if error == "unsupported_format" else 413, error, ERRORS[error])
    data, ext, width, height = processed

    try:
        with transaction.atomic():
            record = ImportRecord(
                api_key=key, external_id=external_id, category=category, purpose=purpose,
                original_name=name[:255], sha256=digest, width=width, height=height,
            )
            record.file.save(f"file.{ext}", ContentFile(data), save=False)
            record.save()
            if purpose == "cover":
                category.cover.save(f"cover-{category.pk}.{ext}", ContentFile(data), save=True)
                record.state = "cover_set"
                record.save(update_fields=["state"])
            elif key.can_create_cards:
                from .services import create_card_from_record

                create_card_from_record(record, publish=key.can_publish)
    except IntegrityError:
        existing = ImportRecord.objects.filter(external_id=external_id).first()
        if existing and existing.sha256 == digest:
            return JsonResponse(_record_payload(existing, duplicate=True))
        return fail(409, "conflict", "Этот external_id уже занят.")

    _log(key, "upload", "accepted", record.get_state_display(), external_id, category.pk, name)
    return JsonResponse(_record_payload(record), status=201)
