"""Health check HTTP endpoints."""

from __future__ import annotations

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.health.serializers import HealthStatusSerializer
from apps.health.services import get_health_status


class HealthzView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        serializer = HealthStatusSerializer(get_health_status())
        return Response({"data": serializer.data, "error": None, "meta": {}})
