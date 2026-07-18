"""Health check serializers."""

from __future__ import annotations

from rest_framework import serializers


class HealthStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class HealthEnvelopeSerializer(serializers.Serializer):
    data = HealthStatusSerializer()  # type: ignore[assignment]
    error = serializers.JSONField(allow_null=True)
    meta = serializers.DictField()
