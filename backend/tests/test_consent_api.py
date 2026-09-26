"""T-003A acceptance: consent API + log + the server-side gate on /api/chat/.

Order (M1-orders-1.md T-003A §Tests): no consent → `me.consent.informed=false` and
`/api/chat/` 403 `consent_required`; POST → 201 + 1 row; POST twice → 2 rows; then chat
200; wrong version/kind → 400 + 0 rows; device B cannot see device A's consent;
GET /api/consent/ → 405; POST without a cookie issues `hid` and logs against the new
identity. Plus the append-only guard and the no-PII shape of the row.
"""

import hashlib
import re

import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.accounts.device import HID_COOKIE
from apps.accounts.models import AnonymousIdentity
from apps.summaries.constants import CURRENT_CONSENT
from apps.summaries.models import Consent

pytestmark = pytest.mark.django_db

CONSENT_BODY = {"kind": "informed", "version": CURRENT_CONSENT["informed"]}


def accept(api: APIClient) -> APIClient:
    response = api.post("/api/consent/", CONSENT_BODY, format="json")
    assert response.status_code == 201, response.content
    return api


# --- the gate -----------------------------------------------------------------


def test_chat_is_403_without_consent_and_me_says_so(api):
    me = api.get("/api/me/")

    assert me.status_code == 200
    assert me.json()["consent"] == {"informed": False, "version": CURRENT_CONSENT["informed"]}
    assert Consent.objects.count() == 0

    chat = api.get("/api/chat/")

    assert chat.status_code == 403
    assert chat.json() == {
        "code": "consent_required",
        "detail": "برای شروع گفت‌وگو ابتدا باید رضایت آگاهانه را بپذیری.",
    }


def test_chat_is_200_after_consent_and_me_reports_it(api):
    accept(api)

    me = api.get("/api/me/")
    assert me.json()["consent"] == {"informed": True, "version": "v1"}

    chat = api.get("/api/chat/")
    assert chat.status_code == 200
    assert chat.json() == {"placeholder": True}


def test_gate_is_per_device(api):
    """Device A's consent never leaks to device B."""
    accept(api)
    assert api.get("/api/chat/").status_code == 200
    identity_a = api.get("/api/me/").json()  # A still consented

    other = APIClient(raise_request_exception=True)
    me_b = other.get("/api/me/")
    assert me_b.json()["consent"] == {"informed": False, "version": "v1"}
    assert other.get("/api/chat/").json()["code"] == "consent_required"

    # B never saw A's consent, and the single audit row belongs to A's identity only.
    assert identity_a["consent"]["informed"] is True
    assert Consent.objects.count() == 1
    assert AnonymousIdentity.objects.count() == 2
    assert Consent.objects.get().identity_id != AnonymousIdentity.objects.exclude(
        id=Consent.objects.get().identity_id
    ).get().id


# --- POST /api/consent/ -------------------------------------------------------


def test_post_creates_one_row_and_returns_contract_body(api):
    response = api.post("/api/consent/", CONSENT_BODY, format="json")

    assert response.status_code == 201
    body = response.json()
    assert set(body.keys()) == {"kind", "version", "accepted_at"}
    assert body["kind"] == "informed"
    assert body["version"] == "v1"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T[\d:.]+Z", body["accepted_at"]), body["accepted_at"]

    row = Consent.objects.get()
    assert row.kind == "informed"
    assert row.version == "v1"
    assert row.identity is not None
    assert row.identity.token_hash == hashlib.sha256(
        api.cookies[HID_COOKIE].value.encode()
    ).hexdigest()


def test_accepting_twice_logs_twice(api):
    accept(api)
    accept(api)

    assert Consent.objects.count() == 2
    assert list(Consent.objects.values_list("kind", flat=True)) == ["informed", "informed"]


@pytest.mark.parametrize(
    "body",
    [
        {"kind": "share", "version": "v1"},  # known kind, but not accepted today
        {"kind": "informed", "version": "v2"},  # wrong version
        {"kind": "informed", "version": ""},
        {"kind": "unknown", "version": "v1"},
        {"kind": "informed"},
        {"version": "v1"},
        {},
        ["informed", "v1"],
    ],
)
def test_invalid_bodies_are_400_with_zero_rows(api, body):
    response = api.post("/api/consent/", body, format="json")

    assert response.status_code == 400, response.content
    assert response.json()["code"] == "invalid_consent"
    assert Consent.objects.count() == 0


def test_get_is_405_in_the_error_envelope(api):
    response = api.get("/api/consent/")

    assert response.status_code == 405
    assert set(response.json().keys()) == {"code", "detail"}
    assert response.json()["code"] == "method_not_allowed"
    assert Consent.objects.count() == 0


def test_post_without_cookie_issues_hid_and_logs_against_it():
    client = APIClient(raise_request_exception=True)
    assert AnonymousIdentity.objects.count() == 0

    response = client.post("/api/consent/", CONSENT_BODY, format="json")

    assert response.status_code == 201
    raw = response.cookies[HID_COOKIE].value
    assert len(raw) == 43
    assert AnonymousIdentity.objects.count() == 1
    identity = AnonymousIdentity.objects.get()
    assert Consent.objects.get().identity_id == identity.id
    assert identity.token_hash == hashlib.sha256(raw.encode()).hexdigest()


def test_consent_requires_json_body(api):
    """§1: JSON only. A form-encoded POST is refused by DRF (415), in the envelope."""
    response = api.post("/api/consent/", CONSENT_BODY)

    assert response.status_code == 415
    assert set(response.json().keys()) == {"code", "detail"}
    assert Consent.objects.count() == 0


# --- audit properties ---------------------------------------------------------


def test_rows_are_append_only(api):
    accept(api)
    row = Consent.objects.get()

    row.version = "v9"
    with pytest.raises(ValidationError):
        row.save()

    assert Consent.objects.get().version == "v1"


def test_row_carries_no_pii(api):
    accept(api)
    assert Consent.objects.count() == 1

    assert [f.name for f in Consent._meta.get_fields() if hasattr(f, "attname")] == [
        "id",
        "identity",
        "kind",
        "version",
        "created_at",
    ]
    assert not any(
        field in {"ip", "user_agent", "email", "phone", "note"}
        for field in {f.name for f in Consent._meta.get_fields()}
    )


def test_audit_survives_identity_deletion(api):
    """SET_NULL: the audit row outlives the anonymous identity (D-S4)."""
    accept(api)
    AnonymousIdentity.objects.all().delete()

    row = Consent.objects.get()
    assert row.identity is None
    assert row.kind == "informed"
