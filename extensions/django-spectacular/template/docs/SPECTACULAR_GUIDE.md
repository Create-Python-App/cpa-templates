# Django Spectacular Guide

This extension adds `drf-spectacular` for OpenAPI 3 schema generation and Swagger UI to your Django API.

Because `create-awesome-python-app` avoids automatically modifying your Python code, you must manually wire the configuration into your `settings.py` and `urls.py`.

## 1. Configure Settings

In `config/settings.py`, add `drf_spectacular` to your `INSTALLED_APPS` and configure the Django REST Framework to use the spectacular schema class.

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "rest_framework",
    "drf_spectacular",
    "apps.health",
]

REST_FRAMEWORK = {
    # ... existing config ...
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Django API",
    "DESCRIPTION": "API scaffolded with create-awesome-python-app",
    "VERSION": "0.1.0",
}
```

## 2. Expose the Schema & Swagger UI

In `config/urls.py`, import the spectacular views and add them to your `urlpatterns`. Ensure that `api_prefix` matches the prefix used in your project.

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ... existing imports and api_prefix ...

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
```

## 3. Documenting Your Endpoints

To generate a detailed and typed OpenAPI schema, you should explicitly document your endpoints. This ensures that the generated Swagger UI accurately reflects the expected request and response shapes, which is crucial for client generation and API exploration.

In your views (e.g., `apps/health/views.py`), import `extend_schema` from `drf_spectacular.utils` and apply it to your endpoint methods. You'll also need to define and import the appropriate serializers.

```python
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.health.serializers import HealthStatusSerializer

# Define an envelope serializer for the response shape
class HealthEnvelopeSerializer(serializers.Serializer):
    data = HealthStatusSerializer()
    error = serializers.JSONField(allow_null=True)
    meta = serializers.DictField()

class HealthzView(APIView):
    # ... existing config ...

    @extend_schema(responses={200: HealthEnvelopeSerializer})
    def get(self, request: Request) -> Response:
        # ... existing implementation ...
        pass
```

## 4. Verify

Run your local development server:

```sh
uv run python manage.py runserver
```

Navigate to `http://localhost:8000/api/v1/docs/` (or your configured `apiPrefix`) to view the interactive Swagger UI!
