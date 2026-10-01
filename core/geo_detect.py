"""Автоопределение города посетителя из РФ — только как предложение на городских страницах.

IP сам по себе ничего не решает: сервер лишь сообщает, какой активный городской лендинг соответствует
определённому городу. Переход и запоминание города происходят после действия посетителя (на стороне браузера).
Страну и город берёт из заголовков, которые добавляет Cloudflare или веб-сервер с геобазой; без настроенного
источника функция молчит.
"""
import re
from urllib.parse import unquote

from django.conf import settings

BOT_RE = re.compile(r"bot|crawl|spider|slurp|yandex|google|bing|baidu|duckduck|facebookexternalhit|preview|lighthouse", re.I)


def _headers():
    provider = (settings.GEO_PROVIDER or "").lower()
    if provider == "cloudflare":
        return "CF-IPCountry", "CF-IPCity"
    if provider == "headers":
        return settings.GEO_COUNTRY_HEADER, settings.GEO_CITY_HEADER
    return None


def norm(value):
    value = unquote(value or "").strip().casefold().replace("ё", "е")
    return re.sub(r"[\s\-_.’']+", " ", value).strip()


def detect(request):
    """(country, city) по заголовкам; (\"\", \"\") если источник не настроен или данных нет."""
    names = _headers()
    if not names or BOT_RE.search(request.META.get("HTTP_USER_AGENT", "")):
        return "", ""
    country = request.headers.get(names[0], "").strip().upper()
    city = request.headers.get(names[1], "").strip()
    return country, city


def landing_key(landing):
    """Безопасный ключ города для cookie selected_city: латинский slug."""
    return (landing.slug_en or "").strip() or str(landing.pk)


def active_landings():
    """Активные русские городские лендинги РФ: опубликованы, есть русский адрес."""
    from content.models import CityLanding

    result = []
    for landing in CityLanding.objects.filter(published=True).select_related("city"):
        if landing.city_id and landing.city.country_code != "RU":
            continue
        if landing.url("ru"):
            result.append(landing)
    return result


def match_landing(city, landings=None):
    """Лендинг для определённого города: только точное совпадение названия или явного названия из админки."""
    wanted = norm(city)
    if not wanted:
        return None
    for landing in landings if landings is not None else active_landings():
        names = {norm(landing.name_ru), norm(landing.name_en)}
        names.update(norm(line) for line in (landing.geo_aliases or "").splitlines() if line.strip())
        if wanted in names:
            return landing
    return None


def picker_items(landings=None):
    items = []
    for landing in landings if landings is not None else active_landings():
        if landing.show_in_picker:
            items.append({"key": landing_key(landing), "name": landing.name_ru, "url": landing.url("ru")})
    return items
