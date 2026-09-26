import re

import pytest
from rest_framework.test import APIClient

HID_RE = re.compile(r"^[A-Za-z0-9_-]{43}$")


@pytest.fixture
def api() -> APIClient:
    return APIClient(raise_request_exception=True)


@pytest.fixture
def set_hid(api: APIClient):
    """Factory: put a `hid` cookie value on the test client."""

    def _set(value: str) -> APIClient:
        api.cookies["hid"] = value
        return api

    return _set
