import hashlib
import logging
import re
from urllib.parse import unquote
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.conf import settings as dj_settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.validators import EmailValidator, ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone, translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from PIL import Image

from catalog.models import Category, Painting, size_option
from content.models import CertificateNominal
from core.labels_runtime import label
from core.models import SiteSettings, StandardSize

from .models import Lead, LeadAttachment

log = logging.getLogger(__name__)

ALLOWED_IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}
MAX_SIDE_CM = Decimal("1000")


def _decimal(value):
    try:
        number = Decimal(str(value).replace(",", ".").strip())
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite() or number <= 0 or number > MAX_SIDE_CM:
        return None
    return number.quantize(Decimal("0.1"))


def _validate_contact(method, value):
    value = value.strip()
    if not value:
        return label("form.error.required")
    if method == "email":
        try:
            EmailValidator()(value)
        except ValidationError:
            return label("form.error.email")
    elif method in ("phone", "whatsapp"):
        digits = re.sub(r"\D", "", value)
        if not 7 <= len(digits) <= 15:
            return label("form.error.phone")
    elif method == "telegram":
        if not re.fullmatch(r"@?[A-Za-z0-9_]{4,32}", value) and not 7 <= len(re.sub(r"\D", "", value)) <= 15:
            return label("form.error.required")
    return None


def _allowed_sizes(painting):
    if painting is not None:
        return {opt["id"]: opt for opt in painting.desired_sizes()}
    return {f"s{s.pk}": size_option(s) for s in StandardSize.objects.filter(visible=True)}


def _check_image(upload):
    max_bytes = dj_settings.LEAD_ATTACHMENT_MAX_MB * 1024 * 1024
    if upload.size > max_bytes:
        return None, label("form.error.file_size")
    try:
        with Image.open(upload) as img:
            fmt = img.format
            img.verify()
    except Exception:  # noqa: BLE001 — любой нераспознанный файл отклоняется
        return None, label("form.error.file_type")
    if fmt not in ALLOWED_IMAGE_FORMATS:
        return None, label("form.error.file_type")
    upload.seek(0)
    return ALLOWED_IMAGE_FORMATS[fmt], None


def _respond(request, ok, payload, status=200):
    wants_json = request.headers.get("x-requested-with") == "fetch"
    if wants_json:
        return JsonResponse({"ok": ok, **payload}, status=status)
    back = request.POST.get("source_url") or "/"
    if not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        back = "/"
    if ok:
        messages.success(request, payload.get("message", ""))
    else:
        messages.error(request, payload.get("message", label("form.error.generic")))
    return HttpResponseRedirect(back)


@require_POST
def submit(request):
    lang = request.POST.get("lang") if request.POST.get("lang") in ("en", "zh") else "ru"
    translation.activate(lang)
    data = request.POST
    site = SiteSettings.get()
    success_message = _success_text(lang)

    # Ловушка для ботов: поле скрыто от людей.
    if data.get("website"):
        return _respond(request, True, {"message": success_message})

    key = (data.get("idempotency_key") or "").strip()[:64] or None
    if key:
        existing = Lead.objects.filter(idempotency_key=key).first()
        if existing:
            return _respond(request, True, {"message": success_message, "lead": existing.pk})

    ip = request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR", "")
    ip_hash = hashlib.sha256((dj_settings.SECRET_KEY + ip).encode()).hexdigest()
    recent = Lead.objects.filter(ip_hash=ip_hash, created_at__gte=timezone.now() - timedelta(minutes=10)).count()
    if recent >= 15:
        return _respond(request, False, {"message": label("form.error.generic")}, status=429)

    errors = {}
    name = data.get("name", "").strip()
    if not name:
        errors["name"] = label("form.error.required")
    method = data.get("contact_method", "")
    if method not in dict(Lead.CONTACT_METHODS):
        errors["contact_method"] = label("form.error.required")
    else:
        contact_error = _validate_contact(method, data.get("contact", ""))
        if contact_error:
            errors["contact"] = contact_error

    if site.consent_checkbox and data.get("consent") not in ("1", "on", "true"):
        errors["consent"] = label("form.error.consent")

    # Контекст определяется на сервере по идентификаторам, а не по тексту из браузера.
    kind = data.get("kind", "general")
    if kind not in dict(Lead.KINDS):
        kind = "general"
    painting = category = None
    if data.get("painting_id", "").isdigit():
        painting = Painting.objects.filter(pk=int(data["painting_id"]), published=True).select_related("category").first()
    if data.get("category_id", "").isdigit():
        category = Category.objects.filter(pk=int(data["category_id"]), visible=True).first()
    if painting is not None:
        kind = "similar" if painting.status == Painting.SOLD else "painting"
        category = painting.category
    elif kind in ("painting", "similar"):
        kind = "category" if category else "general"
    elif category is not None and kind == "general":
        kind = "category"

    lead = Lead(
        kind=kind,
        painting=painting,
        painting_title=painting.title_ru if painting else "",
        painting_status=painting.get_status_display() if painting else "",
        category=category,
        source_url=unquote(data.get("source_url") or "")[:500],
        lang=lang,
        name=name[:120],
        contact_method=method,
        contact=data.get("contact", "").strip()[:160],
        city=data.get("city", "").strip()[:120],
        deadline=data.get("deadline", "").strip()[:120],
        comment=data.get("comment", "").strip()[:5000],
        idempotency_key=key,
        ip_hash=ip_hash,
        consent_given=data.get("consent") in ("1", "on", "true"),
        certificate_recipient=data.get("certificate_recipient", "").strip()[:160],
    )

    # Желаемый размер новой картины (раздел 5.3): значения фиксируются в заявке.
    size_choice = data.get("size_choice", "")
    if size_choice == "standard" and kind not in ("certificate",):
        options = _allowed_sizes(painting)
        option = options.get(data.get("size_id", ""))
        if option is None:
            errors["size_id"] = label("form.error.size")
        else:
            small, large = sorted([option["width"], option["height"]])
            if option["square"]:
                lead.size_width, lead.size_height, lead.size_orientation = small, large, "square"
            else:
                orientation = data.get("size_orientation", "")
                if orientation == "horizontal":
                    lead.size_width, lead.size_height = large, small
                elif orientation == "vertical":
                    lead.size_width, lead.size_height = small, large
                else:
                    errors["size_orientation"] = label("form.error.required")
                lead.size_orientation = orientation
            lead.size_choice = "standard"
    elif size_choice == "custom":
        width, height = _decimal(data.get("size_width", "")), _decimal(data.get("size_height", ""))
        if width is None or height is None:
            errors["size_custom"] = label("form.error.size")
        else:
            lead.size_width, lead.size_height, lead.size_choice = width, height, "custom"
            lead.size_orientation = "square" if width == height else ("horizontal" if width > height else "vertical")
    elif size_choice == "undecided":
        lead.size_choice = "undecided"

    if kind == "certificate":
        raw_amount = data.get("certificate_amount", "")
        if raw_amount == "custom" and site.certificate_custom_amount:
            custom = data.get("certificate_custom", "").replace(" ", "")
            if custom.isdigit() and 0 < int(custom) <= 10_000_000:
                lead.certificate_amount = int(custom)
            else:
                errors["certificate_custom"] = label("form.error.required")
        elif raw_amount.isdigit():
            if CertificateNominal.objects.filter(visible=True, amount=int(raw_amount)).exists():
                lead.certificate_amount = int(raw_amount)
            else:
                errors["certificate_amount"] = label("form.error.required")
        fmt = data.get("certificate_format", "")
        allowed = {f for f, ok in (("electronic", site.certificate_electronic), ("print", site.certificate_print)) if ok}
        if fmt:
            if fmt in allowed:
                lead.certificate_format = fmt
            else:
                errors["certificate_format"] = label("form.error.required")

    upload = request.FILES.get("file")
    ext = None
    if upload:
        ext, file_error = _check_image(upload)
        if file_error:
            errors["file"] = file_error

    if errors:
        return _respond(request, False, {"message": label("form.error.generic"), "errors": errors}, status=400)

    try:
        with transaction.atomic():
            lead.save()
            if upload and ext:
                upload.name = f"upload.{ext}"
                LeadAttachment.objects.create(
                    lead=lead, file=upload, original_name=request.FILES["file"].name[:200], size=upload.size,
                )
    except IntegrityError:
        existing = Lead.objects.filter(idempotency_key=key).first() if key else None
        if existing:
            return _respond(request, True, {"message": success_message, "lead": existing.pk})
        log.exception("Не удалось сохранить заявку")
        return _respond(request, False, {"message": _error_text(lang)}, status=500)
    except Exception:  # noqa: BLE001
        log.exception("Не удалось сохранить заявку")
        return _respond(request, False, {"message": _error_text(lang)}, status=500)

    _notify(lead, site, request)
    return _respond(request, True, {"message": success_message, "lead": lead.pk})


def _success_text(lang):
    from core.models import SharedBlock
    from core.i18n import tr

    block = SharedBlock.objects.filter(key="form-success").first()
    return (tr(block, "text", lang) if block else "") or label("form.ok_title", lang)


def _error_text(lang):
    from core.models import SharedBlock
    from core.i18n import tr

    block = SharedBlock.objects.filter(key="form-error").first()
    return (tr(block, "text", lang) if block else "") or label("form.error.generic", lang)


def _notify(lead, site, request):
    recipients = [e.strip() for e in site.notify_emails.split(",") if e.strip()]
    if not recipients:
        return
    admin_url = site.absolute(f"/{dj_settings.ADMIN_PATH}leads/lead/{lead.pk}/change/", request)
    lines = [
        f"Новая заявка №{lead.pk} на сайте {site.brand('ru')}",
        f"Тип: {lead.get_kind_display()}",
        f"Имя: {lead.name}",
        f"Связь: {lead.get_contact_method_display()} — {lead.contact}",
    ]
    if lead.painting_title:
        lines.append(f"Картина: {lead.painting_title} ({lead.painting_status})")
    if lead.category:
        lines.append(f"Рубрика: {lead.category.name_ru}")
    if lead.size_display:
        lines.append(f"Желаемый размер: {lead.size_display}")
    if lead.certificate_amount or lead.kind == "certificate":
        lines.append(f"Сертификат: {lead.certificate_amount or 'номинал не выбран'} {lead.get_certificate_format_display()}")
    if lead.certificate_recipient:
        lines.append(f"Получатель сертификата: {lead.certificate_recipient}")
    for label_text, value in (("Город", lead.city), ("Срок", lead.deadline), ("Комментарий", lead.comment)):
        if value:
            lines.append(f"{label_text}: {value}")
    lines += ["", f"Открыть в админке: {admin_url}"]
    try:
        send_mail(f"Заявка №{lead.pk} — {site.brand('ru')}", "\n".join(lines), None, recipients, fail_silently=False)
    except Exception as exc:  # noqa: BLE001 — заявка уже сохранена
        log.warning("Уведомление о заявке %s не отправлено: %s", lead.pk, exc)
        Lead.objects.filter(pk=lead.pk).update(notification_error=str(exc)[:255])
