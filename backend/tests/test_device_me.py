"""Order §5 + §6 + §1: device token lifecycle through GET /api/me/.

Covers: first visit → 1 row + cookie flags exactly per §1; revisit → same row,
count 1, last_seen_at advanced, is_new=false; garbage cookie → new row;
DB stores sha256(token) only; Secure flag follows COOKIE_SECURE.
"""

import hashlib
import time

import pytest

from apps.accounts.device import HID_COOKIE, HID_MAX_AGE
from apps.accounts.models import AnonymousIdentity

pytestmark = pytest.mark.django_db


def _morsel(response, key=HID_COOKIE):
    """The test client exposes Set-Cookie via SimpleCookie (headers don't)."""
    return response.cookies[key]


def test_first_visit_creates_row_and_issues_cookie(api):
    assert AnonymousIdentity.objects.count() == 0

    response = api.get("/api/me/")

    assert response.status_code == 200
    assert response.json() == {"anonymous": True, "is_new": True}
    assert AnonymousIdentity.objects.count() == 1

    raw = response.cookies[HID_COOKIE].value
    assert len(raw) == 43  # secrets.token_urlsafe(32) shape
    identity = AnonymousIdentity.objects.get()
    assert identity.token_hash == hashlib.sha256(raw.encode()).hexdigest()
    assert identity.token_hash != raw


def test_cookie_flags_exact(api):
    response = api.get("/api/me/")

    m = _morsel(response)
    assert m.key == HID_COOKIE
    assert m["httponly"]
    assert m["samesite"].lower() == "lax"
    assert m["path"] == "/"
    assert int(m["max-age"]) == HID_MAX_AGE  # 31536000
    assert not m["secure"]  # COOKIE_SECURE=0 locally

    wire = m.output().lower()  # the flag string as the wire sees it
    for flag in ("httponly", "samesite=lax", "path=/", "max-age=31536000"):
        assert flag in wire
    assert "secure" not in wire


def test_cookie_secure_flag_follows_env(api, settings):
    settings.COOKIE_SECURE = True

    response = api.get("/api/me/")

    assert _morsel(response)["secure"]


def test_revisit_resumes_same_identity_and_advances_last_seen(api):
    first = api.get("/api/me/")
    raw = first.cookies[HID_COOKIE].value
    identity_before = AnonymousIdentity.objects.get()
    created_at = identity_before.created_at
    last_seen = identity_before.last_seen_at

    api.cookies[HID_COOKIE] = raw
    time.sleep(0.05)  # ensure the clock visibly moves
    second = api.get("/api/me/")

    assert second.status_code == 200
    assert second.json() == {"anonymous": True, "is_new": False}
    assert AnonymousIdentity.objects.count() == 1
    identity_after = AnonymousIdentity.objects.get()
    assert identity_after.id == identity_before.id
    assert identity_after.created_at == created_at
    assert identity_after.last_seen_at > last_seen


def test_garbage_cookie_gets_new_identity_not_401(set_hid):
    response = set_hid("garbage-not-a-token").get("/api/me/")

    assert response.status_code == 200
    assert response.json()["is_new"] is True
    assert AnonymousIdentity.objects.count() == 1
    assert response.cookies[HID_COOKIE].value != "garbage-not-a-token"


def test_wellformed_but_unknown_cookie_gets_new_identity(api):
    unknown = "b" * 43  # valid token shape, no row behind it

    api.cookies[HID_COOKIE] = unknown
    response = api.get("/api/me/")

    assert response.status_code == 200
    assert response.json()["is_new"] is True
    assert AnonymousIdentity.objects.count() == 1
    assert response.cookies[HID_COOKIE].value != unknown


def test_me_response_has_exactly_contract_keys(api):
    """T-001 scope: `consent` arrives in T-003A — this locks today's shape."""

    response = api.get("/api/me/")

    assert set(response.json().keys()) == {"anonymous", "is_new"}
