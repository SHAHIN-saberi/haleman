"""Error envelope — every DRF error body becomes `{"code", "detail"}` (binding §1, N-1).

Why this exists: DRF answers a 405 with `{"detail": "Method \"POST\" not allowed."}` — no
`code` — and a `ValidationError` with whatever the raiser chose. §1 (D-S6) fixes the body
shape for every `/api/*` error, so the frontend can branch on a stable `code` instead of
matching Persian text. The wrap happens here, once, instead of in every view.

Contract:
- 400/405 (and any other DRF APIException) → `{"code": "<snake_case>", "detail": "<text>"}`;
- the `code` is taken from the exception (a custom `code` on a permission/exception wins,
  otherwise DRF's own: `method_not_allowed`, `not_found`, `unsupported_media_type`, ...);
- existing messages stay byte-identical — only the envelope changes;
- non-DRF exceptions (500) are untouched: DRF returns None and Django handles them.
"""

from rest_framework.views import exception_handler

#: Fallback when DRF hands us something without a usable code.
DEFAULT_CODE = "error"


def _code_of(detail, exc) -> str:
    code = getattr(detail, "code", None)
    if isinstance(code, str) and code:
        return code
    code = getattr(exc, "default_code", None)
    if isinstance(code, str) and code:
        return code
    return DEFAULT_CODE


def envelope_exception_handler(exc, context):
    """DRF `EXCEPTION_HANDLER`: normalize APIException bodies to `{code, detail}`."""
    response = exception_handler(exc, context)
    if response is None:
        return None  # not a DRF exception — let Django produce its own response

    data = response.data
    if isinstance(data, dict) and set(data.keys()) == {"code", "detail"}:
        return response  # already in the contract shape (e.g. raised by us)

    if isinstance(data, dict) and "detail" in data and len(data) == 1:
        detail = data["detail"]
        response.data = {"code": _code_of(detail, exc), "detail": str(detail)}
        return response

    if isinstance(data, dict):
        # Field errors (serializers): keep the field map, add the envelope keys so the
        # client can always read `code` and `detail`.
        response.data = {
            "code": _code_of(None, exc) if getattr(exc, "default_code", None) else "invalid",
            "detail": "درخواست نامعتبر است.",
            "fields": data,
        }
        return response

    response.data = {"code": _code_of(None, exc), "detail": str(data)}
    return response
