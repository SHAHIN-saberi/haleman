"""Haleman URL configuration — every endpoint under /api/ with a trailing slash (D-S6)."""

from django.urls import path

from apps.accounts.views import MeView, health
from apps.chat.views import ChatPlaceholderView
from apps.summaries.views import ConsentView

urlpatterns = [
    path("api/health/", health, name="health"),
    path("api/me/", MeView.as_view(), name="me"),
    path("api/consent/", ConsentView.as_view(), name="consent"),
    path("api/chat/", ChatPlaceholderView.as_view(), name="chat"),
]
