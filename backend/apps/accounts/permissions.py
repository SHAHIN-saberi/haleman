"""Consent gate — the server-side check that `/api/chat/` requires (D-S6, product rule 2/3).

The frontend never decides this. `HasInformedConsent` is a DRF permission so the 403
body goes through the project's exception envelope (config/exception_handler.py):
`{"code": "consent_required", "detail": "…"}`.
"""

from rest_framework.permissions import BasePermission

from apps.accounts.contract import serves_method
from apps.summaries.constants import CURRENT_CONSENT
from apps.summaries.models import Consent


def consent_state(identity) -> dict:
    """`{"informed": bool, "version": str | None}` — the shape `/api/me/` returns (§1).

    Only the *current* version counts as consented: a bumped version means every device
    is asked again, which is why the version lives in the query, not in the client.
    """
    if identity is None:
        return {"informed": False, "version": None}
    wanted = CURRENT_CONSENT["informed"]
    row = (
        Consent.objects.filter(identity=identity, kind="informed", version=wanted)
        .order_by("-created_at")
        .values_list("version", flat=True)
        .first()
    )
    return {"informed": row is not None, "version": row if row is not None else wanted}


class HasInformedConsent(BasePermission):
    """Allow only identities that accepted the current `informed` consent version.

    `code` is read by DRF's `APIView.permission_denied`, so the 403 carries
    `consent_required` into the project error envelope (§1).
    """

    message = "برای شروع گفت‌وگو ابتدا باید رضایت آگاهانه را بپذیری."
    code = "consent_required"

    def has_permission(self, request, view) -> bool:
        if not serves_method(request):
            # DRF checks permissions *before* the method, and an unimplemented method is
            # refused with 405 by the view. Answering 403 here would both leak the gate to
            # callers who never reach an endpoint and hide the real error.
            return True
        identity = getattr(request, "auth", None)
        return bool(consent_state(identity)["informed"])
