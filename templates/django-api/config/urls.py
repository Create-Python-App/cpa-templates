"""URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

api_prefix = getattr(settings, "API_PREFIX", "/api/v1").lstrip("/")

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path(f"{api_prefix}/", include("apps.health.urls")),
]
