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


class GeoProvider:
    """Источник геоданных: по запросу возвращает (страна, город). Бизнес-логика от источника не зависит."""

    def lookup(self, request):
        return "", ""


class HeadersProvider(GeoProvider):
    """Страну и город передаёт прокси/CDN заголовками."""

    country_header = ""
    city_header = ""

    def lookup(self, request):
        country = request.headers.get(self.country_header, "").strip().upper()
        city = request.headers.get(self.city_header, "").strip()
        return country, city


class CloudflareProvider(HeadersProvider):
    country_header = "CF-IPCountry"
    city_header = "CF-IPCity"  # приходит с включённой настройкой Cloudflare «Add visitor location headers»


class CustomHeadersProvider(HeadersProvider):
    @property
    def country_header(self):
        return settings.GEO_COUNTRY_HEADER

    @property
    def city_header(self):
        return settings.GEO_CITY_HEADER


class SypexProvider(GeoProvider):
    """Место для Sypex Geo City (локальный файл SxGeoCity.dat, GEO_SYPEX_PATH).

    Читатель файла подключается здесь, когда файл будет передан; пока источник ничего не определяет,
    сайт работает как обычно. Остальной код (сопоставление, панель, форма) менять не нужно.
    """

    def lookup(self, request):
        return "", ""


PROVIDERS = {"cloudflare": CloudflareProvider, "headers": CustomHeadersProvider, "sypex": SypexProvider}


def get_provider():
    cls = PROVIDERS.get((settings.GEO_PROVIDER or "").lower())
    return cls() if cls else None


def norm(value):
    value = unquote(value or "").strip().casefold().replace("ё", "е")
    return re.sub(r"[\s\-_.’']+", " ", value).strip()


def detect(request):
    """(страна, город) от настроенного источника; (\"\", \"\") если источник не настроен, это робот или данных нет."""
    provider = get_provider()
    if provider is None or BOT_RE.search(request.META.get("HTTP_USER_AGENT", "")):
        return "", ""
    try:
        return provider.lookup(request)
    except Exception:  # геоисточник не должен мешать работе сайта
        return "", ""


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


def language_by_country(request):
    """Запасной язык по стране IP (когда язык браузера определить нельзя): RU — ru, CN — zh, прочие известные страны — en."""
    country, _ = detect(request)
    if not re.fullmatch(r"[A-Z]{2}", country) or country in ("XX", "T1"):
        return ""
    if country == "RU":
        return "ru"
    return "zh" if country == "CN" else "en"
