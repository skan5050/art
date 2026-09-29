"""
Настройки одной установки сайта.

Каждый сайт (A «МираМе», D «ХолСтори») — отдельная установка одного и того же
кода со своим файлом окружения: своя база, медиатека, секреты и тема.
Значения читаются из переменных окружения; для локального запуска можно
положить их в файл .env рядом с manage.py (см. .env.example).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(Path(os.environ.get("ART_ENV_FILE", BASE_DIR / ".env")))


def env(name, default=None):
    return os.environ.get(name, default)


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


# Тема оформления: "a" — «Голубая акварель» (МираМе), "d" — «Арт-пространство» (ХолСтори).
SITE_THEME = env("SITE_THEME", "a").lower()
if SITE_THEME not in {"a", "d"}:
    raise RuntimeError("SITE_THEME должен быть 'a' или 'd'")

DEBUG = env_bool("DEBUG", False)
SECRET_KEY = env("SECRET_KEY") or ("dev-insecure-key-" + SITE_THEME if DEBUG else None)
if not SECRET_KEY:
    raise RuntimeError("Не задан SECRET_KEY")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")

# Путь админки задается в окружении установки, чтобы не держать его жестко в коде.
ADMIN_PATH = env("ADMIN_PATH", "admin").strip("/") + "/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "catalog",
    "content",
    "leads",
    "geo",
    "importapi",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.CanonicalHostMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "artsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Шаблоны выбранной темы имеют приоритет над общими.
        "DIRS": [BASE_DIR / "templates" / "themes" / SITE_THEME, BASE_DIR / "templates" / "common"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
            "builtins": ["core.templatetags.site_tags"],
        },
    },
]

WSGI_APPLICATION = "artsite.wsgi.application"

DATA_DIR = Path(env("DATA_DIR", BASE_DIR / "var" / SITE_THEME))
DATA_DIR.mkdir(parents=True, exist_ok=True)

if env("DB_ENGINE", "sqlite") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST", "127.0.0.1"),
            "PORT": env("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": env("DB_PATH", DATA_DIR / "db.sqlite3"),
            "OPTIONS": {"timeout": 20},
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский"), ("en", "English")]
TIME_ZONE = env("TIME_ZONE", "Asia/Novosibirsk")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static" / "common", BASE_DIR / "static" / "themes" / SITE_THEME]
STATIC_ROOT = Path(env("STATIC_ROOT", DATA_DIR / "static"))

# Публичная медиатека сайта (обработанные изображения).
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("MEDIA_ROOT", DATA_DIR / "media"))
# Закрытое хранилище: вложения заявок, оригиналы импорта. Не раздается веб-сервером.
PRIVATE_MEDIA_ROOT = Path(env("PRIVATE_MEDIA_ROOT", DATA_DIR / "private"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Загрузки: вложение формы — до 10 МБ (раздел 7 ТЗ); импорт — настраивается.
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
LEAD_ATTACHMENT_MAX_MB = int(env("LEAD_ATTACHMENT_MAX_MB", "10"))
IMPORT_MAX_FILE_MB = int(env("IMPORT_MAX_FILE_MB", "40"))
IMPORT_MAX_PIXELS = int(env("IMPORT_MAX_PIXELS", str(80_000_000)))
IMPORT_RATE_PER_MINUTE = int(env("IMPORT_RATE_PER_MINUTE", "60"))

# Почта для уведомлений о заявках (необязательно; заявка сохраняется в любом случае).
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend" if EMAIL_HOST else "django.core.mail.backends.console.EmailBackend",
)
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@localhost")
EMAIL_TIMEOUT = 15

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "art-" + SITE_THEME}}

SESSION_COOKIE_NAME = "sid_" + SITE_THEME
CSRF_COOKIE_NAME = "csrf_" + SITE_THEME
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

if env_bool("HTTPS", not DEBUG):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(env("HSTS_SECONDS", "0"))

# Перенаправлять запросы с другого хоста на основной адрес из «Общих настроек».
ENFORCE_CANONICAL_HOST = env_bool("ENFORCE_CANONICAL_HOST", False)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", "INFO")},
}
