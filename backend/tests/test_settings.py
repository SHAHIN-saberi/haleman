"""Order §3: settings 100% from env; SECRET_KEY required (ImproperlyConfigured).

Environment-sensitive checks run in a subprocess so the already-imported
settings module can't leak state into them.
"""

import json
import os
import subprocess
import sys

RUN = [sys.executable, "-c", "import config.settings as s; import json; print(json.dumps({"
       "'DEBUG': s.DEBUG, 'ALLOWED_HOSTS': s.ALLOWED_HOSTS, 'ENGINE': "
       "s.DATABASES['default']['ENGINE'], 'USE_TZ': s.USE_TZ, 'TIME_ZONE': s.TIME_ZONE, "
       "'LANGUAGE_CODE': s.LANGUAGE_CODE, 'SECURE_PROXY_SSL_HEADER': "
       "list(s.SECURE_PROXY_SSL_HEADER), 'COOKIE_SECURE': s.COOKIE_SECURE}))"]


def _subprocess_settings(env_overrides: dict) -> dict:
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in {"DJANGO_SECRET_KEY", "DJANGO_DEBUG", "DJANGO_ALLOWED_HOSTS",
                     "CSRF_TRUSTED_ORIGINS", "COOKIE_SECURE", "POSTGRES_DB", "POSTGRES_USER",
                     "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT"}
    }
    env["DJANGO_SECRET_KEY"] = "subprocess-test-key-not-used-in-prod" + "0" * 40
    # Not a placeholder: with DJANGO_DEBUG=0 the settings guard (T-004) rejects `change-me*`.
    env["POSTGRES_PASSWORD"] = "subprocess-test-password"
    env.update(env_overrides)
    proc = subprocess.run(RUN, capture_output=True, text=True, env=env, check=True)
    return json.loads(proc.stdout)


def test_missing_secret_key_raises_improperly_configured():
    env = {k: v for k, v in os.environ.items() if k != "DJANGO_SECRET_KEY"}

    proc = subprocess.run(
        [sys.executable, "-c", "import config.settings"],
        capture_output=True,
        text=True,
        env=env,
    )

    assert proc.returncode != 0
    assert "ImproperlyConfigured" in proc.stderr
    assert "DJANGO_SECRET_KEY" in proc.stderr


def test_empty_secret_key_raises_improperly_configured():
    proc = subprocess.run(
        [sys.executable, "-c", "import config.settings"],
        capture_output=True,
        text=True,
        env={**os.environ, "DJANGO_SECRET_KEY": ""},
    )

    assert proc.returncode != 0
    assert "ImproperlyConfigured" in proc.stderr


def test_defaults_debug_off_postgres_only_fa_utc():
    data = _subprocess_settings({})

    assert data["DEBUG"] is False  # DJANGO_DEBUG default "0"
    assert data["ENGINE"] == "django.db.backends.postgresql"  # no sqlite fallback (TD-03)
    assert data["ALLOWED_HOSTS"] == ["localhost", "127.0.0.1"]
    assert data["USE_TZ"] is True
    assert data["TIME_ZONE"] == "UTC"
    assert data["LANGUAGE_CODE"] == "fa"
    assert data["SECURE_PROXY_SSL_HEADER"] == ["HTTP_X_FORWARDED_PROTO", "https"]
    assert data["COOKIE_SECURE"] is False


def test_debug_and_cookie_secure_parse_from_env():
    data = _subprocess_settings({"DJANGO_DEBUG": "1", "COOKIE_SECURE": "1"})

    assert data["DEBUG"] is True
    assert data["COOKIE_SECURE"] is True


def test_installed_apps_stateless():
    import django.conf as djconf

    apps = djconf.settings.INSTALLED_APPS
    assert "django.contrib.admin" not in apps
    assert "django.contrib.sessions" not in apps
    middleware = djconf.settings.MIDDLEWARE
    assert not any("Session" in m or "Csrf" in m or "Authentication" in m for m in middleware)


# --- placeholder guard (T-004 amendment c) -------------------------------------
# `.env.example` ships `change-me…`; in production mode that must stop the boot, and
# with DJANGO_DEBUG=1 it stays allowed (local hacking without `make env`).

REAL_KEY = "subprocess-test-key-not-used-in-prod" + "0" * 40


def _run_settings(env_overrides: dict):
    env = {k: v for k, v in os.environ.items() if k not in {
        "DJANGO_SECRET_KEY", "DJANGO_DEBUG", "POSTGRES_PASSWORD", "POSTGRES_HOST",
        "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PORT", "CSRF_TRUSTED_ORIGINS",
    }}
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, "-c", "import config.settings"], capture_output=True, text=True, env=env
    )


def test_placeholder_secret_key_refused_when_debug_off():
    proc = _run_settings({
        "DJANGO_SECRET_KEY": "change-me-50-chars-min",
        "POSTGRES_PASSWORD": "real-password",
        "DJANGO_DEBUG": "0",
    })

    assert proc.returncode != 0
    assert "DJANGO_SECRET_KEY" in proc.stderr and "make env" in proc.stderr


def test_placeholder_db_password_refused_when_debug_off():
    proc = _run_settings({
        "DJANGO_SECRET_KEY": REAL_KEY,
        "POSTGRES_PASSWORD": "change-me",
        "DJANGO_DEBUG": "0",
    })

    assert proc.returncode != 0
    assert "POSTGRES_PASSWORD" in proc.stderr


def test_placeholders_allowed_with_debug_on():
    proc = _run_settings({
        "DJANGO_SECRET_KEY": "change-me-50-chars-min",
        "POSTGRES_PASSWORD": "change-me",
        "DJANGO_DEBUG": "1",
    })

    assert proc.returncode == 0, proc.stderr


def test_real_values_pass_in_production_mode():
    proc = _run_settings({
        "DJANGO_SECRET_KEY": REAL_KEY,
        "POSTGRES_PASSWORD": "a-real-password",
        "DJANGO_DEBUG": "0",
    })

    assert proc.returncode == 0, proc.stderr
