"""Example views — after copy, import from apps.<feature_name>.*."""

from __future__ import annotations

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# from apps.<feature_name>.serializers import ExampleSerializer
# from apps.<feature_name>.services import example_message
from .serializers import ExampleSerializer
from .services import example_message


class ExampleView(APIView):
    def get(self, request: Request) -> Response:
        serializer = ExampleSerializer(example_message())
        return Response({"data": serializer.data, "error": None, "meta": {}})
