# API

## Health

`GET {{ apiPrefix }}/healthz/`

```json
{
  "data": { "status": "healthy" },
  "error": null,
  "meta": {}
}
```

## OpenAPI

| Path | Purpose |
|------|---------|
| `{{ apiPrefix }}/schema/` | OpenAPI 3 schema (drf-spectacular) |
| `{{ apiPrefix }}/docs/` | Swagger UI |

Keep DRF serializers as the source of truth for request/response shapes; Spectacular
reads them via `DEFAULT_SCHEMA_CLASS`.
