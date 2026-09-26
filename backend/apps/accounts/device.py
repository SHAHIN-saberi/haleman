"""Device-token service (order §5) — one place that reads/writes the `hid` cookie.

Contract (D-S6 + M1-orders-1.md §1):
- opaque token: `secrets.token_urlsafe(32)`;
- DB stores only sha256(token) hex;
- cookie flags: HttpOnly, SameSite=Lax, Path=/, Max-Age=31536000,
  Secure only when settings.COOKIE_SECURE;
- unknown or garbage cookie → new identity + new cookie, NEVER 401.
"""

import hashlib
import re
import secrets

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from apps.accounts.models import AnonymousIdentity

HID_COOKIE = "hid"
HID_MAX_AGE = 31_536_000  # one year, in seconds

# secrets.token_urlsafe(32) always yields exactly 43 URL-safe base64 chars.
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{43}$")


def new_token() -> str:
    """Issue a fresh opaque device token (raw — for the cookie only)."""
    return secrets.token_urlsafe(32)


def hash_token(raw: str) -> str:
    """sha256 hex of the raw token — the ONLY representation we store."""
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def resolve_or_issue(request: HttpRequest) -> tuple[AnonymousIdentity, str | None]:
    """Resume the identity behind a valid `hid` cookie, or issue a new one.

    Returns `(identity, new_token)`:
    - valid cookie + known row  → (row, None); `last_seen_at` is refreshed;
    - missing / malformed / unknown cookie → (new row, raw token) and the
      caller MUST attach the token to the response via `set_hid_cookie`.
    """
    raw = request.COOKIES.get(HID_COOKIE, "")
    if raw and _TOKEN_RE.fullmatch(raw):
        identity = (
            AnonymousIdentity.objects.filter(token_hash=hash_token(raw))
            .only("id", "token_hash", "created_at", "last_seen_at")
            .first()
        )
        if identity is not None:
            identity.save(update_fields=["last_seen_at"])  # auto_now → fresh stamp
            return identity, None
    token = new_token()
    identity = AnonymousIdentity.objects.create(token_hash=hash_token(token))
    return identity, token


def set_hid_cookie(response: HttpResponse, raw_token: str) -> None:
    """Attach the device cookie with the exact §1 flags (call only on issue)."""
    response.set_cookie(
        HID_COOKIE,
        raw_token,
        max_age=HID_MAX_AGE,
        httponly=True,
        samesite="Lax",
        path="/",
        secure=settings.COOKIE_SECURE,
    )
