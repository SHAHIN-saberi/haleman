"""Consent vocabulary — the single place that defines what "consented" means.

`kind` values are fixed in the M1 contract (D-S4, M1-orders-1.md §1):
  - `informed` — the 3-line W-02 consent; this is what gates `/api/chat/` today.
  - `share`    — leaving the summary to a therapist; only used from T-022.

`version` is a code constant on purpose: it is part of the audit record, it must be
reviewable in git, and a mis-set environment variable must never change what the user
consented to. Bumping a version is a deliberate, reviewed code change.
"""

CURRENT_CONSENT: dict[str, str] = {
    "informed": "v1",
}

#: Consent kinds the API accepts today (`share` exists in the model for T-022).
ACCEPTED_KINDS = frozenset(CURRENT_CONSENT)
