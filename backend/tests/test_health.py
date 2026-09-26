"""Order §4 + F9: GET /api/health/ → 200 {"ok": true}, no auth, no DB row, no Set-Cookie."""

import pytest

from apps.accounts.models import AnonymousIdentity

pytestmark = pytest.mark.django_db


def test_health_returns_ok(api):
    response = api.get("/api/health/")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_health_is_json_only(api):
    response = api.get("/api/health/")

    assert response["Content-Type"].startswith("application/json")


def test_health_never_sets_cookie_and_never_touches_db(api):
    api.cookies["hid"] = "x" * 43  # even with a cookie presented

    response = api.get("/api/health/")

    assert response.status_code == 200
    assert len(response.cookies) == 0  # no Set-Cookie of ANY kind (F9)
    assert AnonymousIdentity.objects.count() == 0


def test_health_rejects_post(api):
    response = api.post("/api/health/")

    assert response.status_code == 405
