"""N-1 (from `reports/senior/M1-review-2.md`): every DRF error body is `{code, detail}`.

Binding contract: M1-orders-1.md §1. The check is deliberately endpoint-wide — a new
endpoint that drifts from the envelope should fail here, not in the frontend.
"""

import pytest

from apps.accounts.models import AnonymousIdentity

pytestmark = pytest.mark.django_db


def assert_envelope(response, status, code):
    assert response.status_code == status, response.content
    body = response.json()
    assert set(body.keys()) == {"code", "detail"}, body
    assert body["code"] == code
    assert isinstance(body["detail"], str) and body["detail"], body


def test_method_not_allowed_on_every_m1_endpoint(api):
    api.get("/api/me/")  # issue the cookie so the request is a normal one

    with_body = api.post("/api/health/", {"k": "v"}, format="json")
    without_body = api.post("/api/health/")
    for response in (with_body, without_body):
        assert_envelope(response, 405, "method_not_allowed")

    assert_envelope(api.get("/api/consent/"), 405, "method_not_allowed")
    assert_envelope(api.post("/api/chat/", {}, format="json"), 405, "method_not_allowed")


def test_health_stays_identity_free_even_when_it_405s(api):
    """F9 + N-2: a rejected method must not create a row or a cookie."""
    response = api.post("/api/health/", {}, format="json")

    assert_envelope(response, 405, "method_not_allowed")
    assert AnonymousIdentity.objects.count() == 0
    assert "set-cookie" not in {k.lower() for k in response.headers}


def test_unchanged_methods_do_not_create_identities(api):
    """N-2: POST/PUT to a GET-only endpoint must not resolve-or-issue an identity."""
    for method in ("post", "put", "patch", "delete"):
        response = getattr(api, method)("/api/me/")
        assert_envelope(response, 405, "method_not_allowed")

    assert AnonymousIdentity.objects.count() == 0


def test_unsupported_media_type_is_in_the_envelope(api):
    assert_envelope(api.post("/api/consent/", {"kind": "informed"}), 415, "unsupported_media_type")


def test_consent_required_is_in_the_envelope(api):
    assert_envelope(api.get("/api/chat/"), 403, "consent_required")


def test_invalid_consent_is_in_the_envelope(api):
    assert_envelope(api.post("/api/consent/", {"kind": "nope", "version": "v1"}, format="json"),
                    400, "invalid_consent")


def test_unknown_api_path_is_not_wrapped_by_us(api):
    """A 404 from the URL resolver is Django's, not DRF's — recorded so nobody assumes otherwise."""
    response = api.get("/api/does-not-exist/")

    assert response.status_code == 404
    assert len(AnonymousIdentity.objects.all()) in (0, 1)  # whatever the client had


# --- the handler itself (unit level) -------------------------------------------


def test_field_errors_keep_the_map_and_gain_the_envelope():
    """Serializer-style field errors stay inspectable: envelope keys + `fields`."""
    from rest_framework.exceptions import ValidationError

    from config.exception_handler import envelope_exception_handler

    exc = ValidationError({"kind": ["required"]})
    result = envelope_exception_handler(exc, {})

    assert result is not None
    assert result.status_code == 400
    assert result.data["code"] == "invalid"
    assert result.data["fields"] == {"kind": ["required"]}
    assert isinstance(result.data["detail"], str) and result.data["detail"]


def test_handler_returns_none_for_non_drf_exceptions():
    from config.exception_handler import envelope_exception_handler

    assert envelope_exception_handler(ValueError("boom"), {}) is None
