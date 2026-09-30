"""Производные версии изображений: без обрезки, с сохранением пропорций и цветового профиля."""
import hashlib
import io
import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from PIL import Image, ImageOps

log = logging.getLogger(__name__)

THUMB_DIR = "cache"


def _source_path(field_file):
    try:
        return Path(field_file.path)
    except (ValueError, NotImplementedError):
        return None


def dimensions(field_file):
    path = _source_path(field_file)
    if path is None or not path.exists():
        return None
    key = "dim:" + hashlib.sha1(f"{path}:{path.stat().st_mtime_ns}".encode()).hexdigest()
    dims = cache.get(key)
    if dims is None:
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                dims = img.size
        except Exception:  # noqa: BLE001 — поврежденный файл не должен ронять страницу
            log.warning("Не удалось прочитать изображение %s", path)
            return None
        cache.set(key, dims, 3600)
    return dims


def thumbnail_url(field_file, width):
    """URL уменьшенной версии шириной до width (WEBP). Оригинал не меняется."""
    path = _source_path(field_file)
    if path is None or not path.exists():
        return ""
    stamp = hashlib.sha1(f"{field_file.name}:{path.stat().st_mtime_ns}:{width}".encode()).hexdigest()[:12]
    # В адресе сохраняем осмысленное имя исходного файла (ТЗ 1.3, Е1); хеш нужен только для обновления версий.
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", path.stem).strip("-_")[:48] or "image"
    rel = f"{THUMB_DIR}/{stem}-{stamp}-{width}.webp"
    target = Path(settings.MEDIA_ROOT) / rel
    if not target.exists():
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                icc = img.info.get("icc_profile")
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if "transparency" in img.info or img.mode in ("LA", "P") else "RGB")
                if img.width > width:
                    height = round(img.height * width / img.width)
                    img = img.resize((width, height), Image.LANCZOS)
                target.parent.mkdir(parents=True, exist_ok=True)
                buffer = io.BytesIO()
                params = {"quality": 86, "method": 5}
                if icc:
                    params["icc_profile"] = icc
                img.save(buffer, "WEBP", **params)
                tmp = target.with_suffix(".tmp")
                tmp.write_bytes(buffer.getvalue())
                tmp.replace(target)
        except Exception:  # noqa: BLE001
            log.exception("Не удалось создать миниатюру %s", path)
            return field_file.url
    return settings.MEDIA_URL + rel
