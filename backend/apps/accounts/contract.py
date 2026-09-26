"""Contract helper: does this request target a method the resolved view implements?

Used by two places that must agree:
- `apps.accounts.authentication.DeviceAuthentication` — N-2: never touch the database for a
  method the view does not implement (no row, no cookie, not even a lookup);
- `apps.accounts.permissions.HasInformedConsent` — do not answer a consent 403 for a method
  that is about to be refused with 405 anyway (DRF checks permissions before it checks the
  method, so without this the caller would get a misleading `not_authenticated` 403).

`allowed_methods` is Django's own list for the view instance, so it always matches reality.
"""


def resolved_view(request):
    """The view instance DRF is dispatching to, or None (bare Request in a unit test)."""
    context = getattr(request, "parser_context", None) or {}
    return context.get("view")


def serves_method(request) -> bool:
    """True when the resolved view implements this HTTP method.

    Permissive when the view is unknown — the guard exists to *narrow* database side
    effects for real requests, not to break unit tests that build a Request by hand.
    """
    view = resolved_view(request)
    allowed = getattr(view, "allowed_methods", None)
    if not allowed:
        return True
    return request.method.upper() in {method.upper() for method in allowed}
