"""Health check serializers."""

from __future__ import annotations

from rest_framework import serializers


class HealthStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
