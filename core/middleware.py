from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils import translation

from . import labels_runtime


class CanonicalHostMiddleware:
    """Язык по адресу (/en/ — английская версия) и единая версия хоста.

    Перенаправление на основной хост включается ENFORCE_CANONICAL_HOST;
    обычно это делает веб-сервер (см. docs/deploy.md).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        labels_runtime.reset()
        path = request.path_info
        if path == "/zh" or path.startswith("/zh/"):
            lang = "zh"
        else:
            lang = "en" if path == "/en" or path.startswith("/en/") else "ru"
        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        if settings.ENFORCE_CANONICAL_HOST and not path.startswith(("/" + settings.ADMIN_PATH, "/api/")):
            from .models import SiteSettings

            base = SiteSettings.get().base_url
            if base:
                scheme, _, host = base.partition("://")
                if request.get_host() != host or request.scheme != scheme:
                    return HttpResponsePermanentRedirect(f"{base}{request.get_full_path()}")

        response = self.get_response(request)
        response.headers.setdefault("Content-Language", lang)
        translation.deactivate()
        return response
