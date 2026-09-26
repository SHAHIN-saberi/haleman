"""Haleman URL configuration — every endpoint under /api/ with a trailing slash (D-S6)."""

from django.urls import path

from apps.accounts.views import MeView, health

urlpatterns = [
    path("api/health/", health, name="health"),
    path("api/me/", MeView.as_view(), name="me"),
]
