"""IndexNow: автоматическое уведомление Яндекса об опубликованных, обновленных и удаленных адресах.

Выключено по умолчанию (настройка «Сообщать Яндексу об изменениях»). Отправка идет в отдельном потоке
после сохранения; сбой сети не мешает работе админки и только пишется в журнал.
"""
import json
import logging
import threading
import time
import urllib.request

from django.conf import settings as django_settings
from django.db import transaction

from .i18n import LANGS
from .models import SiteSettings

log = logging.getLogger(__name__)

ENDPOINT = "https://yandex.com/indexnow"
MAX_URLS = 10000
DEDUPE_SECONDS = 60
_recent = {}


def config():
    """(ключ, адрес сайта) или None, если отправка выключена или не настроена."""
    row = SiteSettings.objects.filter(pk=1, indexnow_enabled=True).values("indexnow_key", "base_url").first()
    if not row or not row["indexnow_key"] or not row["base_url"].startswith(("http://", "https://")):
        return None
    return row["indexnow_key"], row["base_url"]


def object_paths(obj):
    """Адреса материала по всем языкам, на которых он существует."""
    return [p for p in (obj.url(code) for code in LANGS if obj.has_lang(code)) if p]


def payload(key, base_url, paths):
    host = base_url.split("://", 1)[1].split("/", 1)[0]
    return {
        "host": host,
        "key": key,
        "keyLocation": f"{base_url}/{key}.txt",
        "urlList": [f"{base_url}{path}" for path in paths][:MAX_URLS],
    }


def send(data):
    request = urllib.request.Request(
        getattr(django_settings, "INDEXNOW_ENDPOINT", ENDPOINT),
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            log.info("IndexNow: %s адресов, ответ %s", len(data["urlList"]), response.status)
    except Exception as exc:  # noqa: BLE001 — уведомление не должно ломать сохранение
        log.warning("IndexNow: не удалось отправить %s адресов: %s", len(data["urlList"]), exc)


def notify(paths):
    """Сообщить об адресах; повтор одного адреса чаще раза в минуту пропускается."""
    conf = config()
    if not conf or not paths:
        return False
    now = time.monotonic()
    fresh = []
    for path in dict.fromkeys(paths):
        if now - _recent.get(path, -DEDUPE_SECONDS) >= DEDUPE_SECONDS:
            _recent[path] = now
            fresh.append(path)
    if not fresh:
        return False
    data = payload(*conf, fresh)
    transaction.on_commit(lambda: threading.Thread(target=send, args=(data,), daemon=True).start())
    return True


def object_saved(obj):
    """Опубликованный материал сохранен: сообщить его адреса (черновики и скрытые страницы не отправляются)."""
    if config() is None:
        return
    from .views import is_public

    if is_public(obj):
        notify(object_paths(obj))
