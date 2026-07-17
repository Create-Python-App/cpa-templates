from django.urls import path

from api.views import HealthzView

urlpatterns = [
    path("healthz", HealthzView.as_view(), name="healthz"),
]
