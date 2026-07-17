"""API views for the django-api starter."""

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthzView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):  # noqa: ARG002
        return Response(
            {
                "data": {"status": "healthy"},
                "message": "Service is healthy",
            }
        )


class PingView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):  # noqa: ARG002
        return Response({"status": "ok"})
