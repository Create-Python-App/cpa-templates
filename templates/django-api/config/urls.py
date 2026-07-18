"""URL configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_prefix = getattr(settings, "API_PREFIX", "/api/v1").lstrip("/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{api_prefix}/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(f"{api_prefix}/", include("apps.health.urls")),
]
