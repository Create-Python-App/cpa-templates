"""URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api_prefix = getattr(settings, "API_PREFIX", "/api/v1").lstrip("/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", include("api.urls_ping")),
    path(f"{api_prefix}/", include("api.urls")),
]
