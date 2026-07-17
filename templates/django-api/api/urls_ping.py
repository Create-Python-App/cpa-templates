from django.urls import path

from api.views import PingView

urlpatterns = [
    path("", PingView.as_view(), name="ping"),
]
