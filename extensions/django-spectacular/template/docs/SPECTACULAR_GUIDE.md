# Django Spectacular Guide

This extension adds `drf-spectacular` for OpenAPI 3 schema generation and Swagger UI to your Django API.

**No manual wiring required.** When you scaffold with `django-spectacular`, CPA automatically appends the necessary configuration to `config/settings.py` and the schema endpoints to `config/urls.py`.

## What gets wired in automatically

**`config/settings.py`** receives:

```python
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
SPECTACULAR_SETTINGS = {
    "TITLE": "Django API",
    "DESCRIPTION": "API scaffolded with create-awesome-python-app",
    "VERSION": "0.1.0",
}
```

**`config/urls.py`** receives:

```python
urlpatterns += [
    path(f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(f"{api_prefix}/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
```

## Verify

Start the development server:

```sh
uv run python manage.py runserver
```

Then open:

- **Swagger UI**: `http://localhost:8000/api/v1/docs/`
- **Raw OpenAPI schema**: `http://localhost:8000/api/v1/schema/`

## Documenting your endpoints with `@extend_schema`

`drf-spectacular` infers response schemas from your serializers automatically. For richer docs, use the `@extend_schema` decorator from `drf_spectacular.utils`:

```python
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.health.serializers import HealthStatusSerializer


class HealthzView(APIView):
    @extend_schema(
        responses={200: HealthStatusSerializer},
        summary="Health check",
        description="Returns the current service health status.",
    )
    def get(self, request: Request) -> Response:
        ...
```

See the [drf-spectacular docs](https://drf-spectacular.readthedocs.io/) for the full decorator API including request body, parameters, and tags.

## Customising `SPECTACULAR_SETTINGS`

Override any key in `config/settings.py` after the auto-wired block:

```python
SPECTACULAR_SETTINGS["TITLE"] = "My Project API"
SPECTACULAR_SETTINGS["VERSION"] = "2.0.0"
```

Full list of available settings: [drf-spectacular configuration reference](https://drf-spectacular.readthedocs.io/en/latest/settings.html).
