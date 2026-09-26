"""Haleman settings — 100% from environment (T-001, TD-03: Postgres only, local = prod).

Contract (reports/senior/M1-orders-1.md T-001 #3):
- no sqlite fallback; every knob below comes from the environment;
- no django.contrib.admin, no sessions middleware — the device flow is stateless;
- timezone UTC, UI language fa, aware datetimes only.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    return default if value is None else value


def _env_bool(name: str, default: str = "0") -> bool:
    return _env(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in _env(name, default).split(",") if item.strip()]


# --- core -------------------------------------------------------------------

# Required (F6/T-001): refuse to boot without a real secret.
SECRET_KEY = _env("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY is missing or empty. Set it via the environment "
        "(.env locally, compose env_file in deployment) — never in code."
    )

DEBUG = _env_bool("DJANGO_DEBUG")

ALLOWED_HOSTS = _env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

CSRF_TRUSTED_ORIGINS = _env_list("CSRF_TRUSTED_ORIGINS")

# --- application registry ----------------------------------------------------

INSTALLED_APPS = [
    "rest_framework",
    "apps.accounts",
    "apps.chat",
    "apps.summaries",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]
# Deliberately NO SessionMiddleware / CsrfViewMiddleware / AuthenticationMiddleware:
# M1 auth is a stateless HttpOnly device cookie (D-S6). DRF APIViews are csrf_exempt;
# JSON-only bodies + SameSite=Lax are the documented M1 CSRF posture (re-visited in T-003A).

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES: list[dict] = []  # API-only in M1; DRF JSONRenderer, no templates

# --- database (Postgres 16 only, TD-03) --------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _env("POSTGRES_DB", "haleman"),
        "USER": _env("POSTGRES_USER", "haleman"),
        "PASSWORD": _env("POSTGRES_PASSWORD", "change-me"),
        "HOST": _env("POSTGRES_HOST", "db"),
        "PORT": _env("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 0,  # no sticky connections → safe under `--scale api=N`
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- placeholder guard (T-004 amendment c) ------------------------------------
# `.env.example` ships `change-me…` values on purpose: they are obviously wrong, and
# with DEBUG=0 they must stop the boot instead of silently signing cookies / connecting
# to Postgres with a public password. `make env` generates real random values.
if not DEBUG:
    _PLACEHOLDERS = (
        ("DJANGO_SECRET_KEY", SECRET_KEY),
        ("POSTGRES_PASSWORD", DATABASES["default"]["PASSWORD"]),
    )
    for _name, _value in _PLACEHOLDERS:
        if str(_value).strip().lower().startswith("change-me"):
            raise ImproperlyConfigured(
                f"{_name} still has the example value from .env.example and DJANGO_DEBUG=0. "
                "Run `make env` (creates .env with random secrets) or set a real value. "
                "Placeholders are accepted only with DJANGO_DEBUG=1."
            )

# --- i18n / tz ----------------------------------------------------------------

LANGUAGE_CODE = "fa"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- proxy / cookies -----------------------------------------------------------

# Caddy is the ONLY published port and terminates TLS; gunicorn sees X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# `hid` cookie Secure flag (D-S6): 0 for local HTTP, 1 behind HTTPS (deployment).
COOKIE_SECURE = _env_bool("COOKIE_SECURE")

# --- DRF -----------------------------------------------------------------------

REST_FRAMEWORK = {
    # Auth is opt-in per view: /api/health/ must never touch identities (F9),
    # device endpoints mount DeviceAuthentication explicitly.
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    # No contrib.auth app → DRF must not build an AnonymousUser (UNAUTHENTICATED_USER=None).
    "UNAUTHENTICATED_USER": None,
    # Binding §1 (N-1): every DRF error body is normalized to {"code", "detail"}.
    "EXCEPTION_HANDLER": "config.exception_handler.envelope_exception_handler",
}
