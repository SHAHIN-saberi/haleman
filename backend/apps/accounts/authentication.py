"""DRF authentication for the anonymous device flow (order §5).

`DeviceAuthentication` is the single DRF entry point for device-auth endpoints
(T-001: /api/me/ · T-003A: consent + chat). It never raises → never 401s:
an unknown/garbage cookie simply resolves to a freshly issued identity.

DRF authentication cannot touch the response, so when a token was just issued
the raw token is stashed on the request; views mixin `DeviceCookieMixin` to
have it set as the `hid` cookie on the outgoing response (single code path).
"""

from rest_framework.authentication import BaseAuthentication

from apps.accounts.device import resolve_or_issue

NEW_HID_ATTR = "new_hid_token"


class DeviceAuthentication(BaseAuthentication):
    """request.auth = the AnonymousIdentity resolved-or-issued for this request."""

    def authenticate(self, request):
        identity, new_token = resolve_or_issue(request)
        setattr(request, NEW_HID_ATTR, new_token)
        # (user, auth) — there is no User model yet (T-017); the identity is both.
        return identity, identity


class DeviceCookieMixin:
    """APIView mixin: set the `hid` cookie when this request issued a token."""

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        from apps.accounts.device import set_hid_cookie

        new_token = getattr(request, NEW_HID_ATTR, None)
        if new_token:
            set_hid_cookie(response, new_token)
        return response
