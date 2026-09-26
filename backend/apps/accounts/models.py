"""Anonymous device identity — the L0 identity of the progressive auth model.

Privacy (D-S6): the database stores ONLY the sha256 hex of the opaque device
token. The raw token lives solely in the HttpOnly `hid` cookie on the device —
never in a log line, a response body, or the DB. No user FK yet; linking to a
real account is T-017.
"""

import uuid

from django.db import models


class AnonymousIdentity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # sha256(token) hex — 64 chars, unique (a unique index, per order §5).
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "anonymous_identities"
        verbose_name = "anonymous identity"
        verbose_name_plural = "anonymous identities"

    def __str__(self) -> str:
        return f"anon:{self.id}"
