"""`POST /api/consent/` — the one way a device becomes consented (T-003A, US-05).

Every acceptance creates a NEW row (repeats included) so the audit shows what the user
saw, when. Requests are JSON-only (§1); anything the contract does not define gets the
project's `{code, detail}` envelope via config/exception_handler.py.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import DeviceAuthentication, DeviceCookieMixin
from apps.summaries.constants import CURRENT_CONSENT
from apps.summaries.models import Consent


class InvalidConsent(APIException):
    """Unknown `kind`, or a `version` that is not the current one."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invalid_consent"
    default_detail = "نوع یا نسخهٔ رضایت نامعتبر است."


class ConsentView(DeviceCookieMixin, APIView):
    """POST /api/consent/ {"kind": "informed", "version": "v1"} → 201.

    - 201 `{"kind", "version", "accepted_at"}` and exactly one new row;
    - unknown kind/version → 400 `{"code": "invalid_consent", "detail": …}` and NO row;
    - GET (or any other method) → 405 in the same envelope (no method exists).
    """

    authentication_classes = [DeviceAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, dict):
            raise InvalidConsent()
        kind = request.data.get("kind")
        version = request.data.get("version")
        if not isinstance(kind, str) or not isinstance(version, str):
            raise InvalidConsent()
        if CURRENT_CONSENT.get(kind) != version:
            raise InvalidConsent()

        consent = Consent.objects.create(identity=request.auth, kind=kind, version=version)
        return Response(
            {
                "kind": consent.kind,
                "version": consent.version,
                # ISO-8601 UTC with a Z suffix — the shape every consumer can parse.
                "accepted_at": consent.created_at.isoformat().replace("+00:00", "Z"),
            },
            status=status.HTTP_201_CREATED,
        )
