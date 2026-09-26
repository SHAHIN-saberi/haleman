"""Consent log — append-only audit rows (D-S4).

Privacy (product rule 4 + M1-orders-1.md §1): the row stores ONLY *which* consent,
*which version* and *when*. No IP, no user-agent, no free text, no copy of the screen.
The link to the anonymous identity is `SET_NULL` so the audit survives a later
"delete my data" (T-022 decides the final policy; T-003A deletes nothing).
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.models import AnonymousIdentity


class ConsentKind(models.TextChoices):
    INFORMED = "informed", "informed"
    SHARE = "share", "share"


class Consent(models.Model):
    """One row per acceptance. Never updated, never rewritten."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity = models.ForeignKey(
        AnonymousIdentity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="consents",
    )
    kind = models.CharField(max_length=16, choices=ConsentKind.choices)
    version = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "consents"
        ordering = ("created_at",)
        indexes = [
            # The gate asks "does this identity have the CURRENT version of `informed`?"
            # — this index answers exactly that question.
            models.Index(fields=("identity", "kind", "version"), name="consent_gate_idx"),
        ]
        verbose_name = "consent"
        verbose_name_plural = "consents"

    def __str__(self) -> str:
        return f"{self.kind}:{self.version}"

    def save(self, *args, **kwargs):
        """Append-only: an existing row can never be rewritten (audit integrity)."""
        if self.pk is not None and not self._state.adding:
            raise ValidationError(
                "Consent rows are append-only; create a new row instead of updating one."
            )
        return super().save(*args, **kwargs)
