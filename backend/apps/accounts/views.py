"""M1 API views: /api/health/ (order §4) and /api/me/ (order §6, §1 contract)."""

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import NEW_HID_ATTR, DeviceAuthentication, DeviceCookieMixin


@api_view(["GET"])
@authentication_classes([])  # health never resolves identities (F9)
@permission_classes([AllowAny])
def health(request):
    """GET /api/health/ → 200 {"ok": true} — no DB row, no Set-Cookie, ever."""
    return Response({"ok": True})


class MeView(DeviceCookieMixin, APIView):
    """GET /api/me/ — resolves or issues the anonymous device identity.

    Response per §1 (T-001 scope, without the `consent` key — added in T-003A):
        {"anonymous": true, "is_new": bool}
    """

    authentication_classes = [DeviceAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "anonymous": True,
                "is_new": getattr(request, NEW_HID_ATTR, None) is not None,
            }
        )
