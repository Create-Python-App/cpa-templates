"""Example serializers — rename package imports after copying into apps/."""

from __future__ import annotations

from rest_framework import serializers


class ExampleSerializer(serializers.Serializer):
    message = serializers.CharField()
