"""Health feature URLs."""

from django.urls import path

from apps.health.views import HealthzView

urlpatterns = [
    path("healthz/", HealthzView.as_view(), name="healthz"),
]
