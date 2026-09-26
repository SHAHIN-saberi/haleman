"""`GET /api/chat/` — M1 placeholder behind the server-side consent gate (T-003A).

The gate is the whole point of this view: without an accepted `informed` consent row the
API answers 403 `consent_required`, no matter what the client believes. T-006 replaces
the placeholder body with the dialogue engine; the gate stays.
"""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import DeviceAuthentication, DeviceCookieMixin
from apps.accounts.permissions import HasInformedConsent


class ChatPlaceholderView(DeviceCookieMixin, APIView):
    """GET /api/chat/ → 200 {"placeholder": true} · 403 {"code": "consent_required"}."""

    authentication_classes = [DeviceAuthentication]
    permission_classes = [AllowAny, HasInformedConsent]

    def get(self, request, *args, **kwargs):
        return Response({"placeholder": True})
