# Testing Guide

## Running tests

```bash
uv sync
uv run pytest
uv run pytest -q
uv run pytest --cov=app --cov-report=term-missing
```

Complementary quality checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app      # when configured — see TYPING.md
uv run pyright       # when configured — see TYPING.md
```

## Test layout

The starter ships a focused suite next to the feature modules:

```text
tests/
  test_health.py    # Health feature + CORS smoke coverage
```

As the API grows, mirror the feature-based app layout:

```text
tests/
  conftest.py
  features/
    test_health.py
    test_<feature>.py
  core/
    test_middleware.py
```

## Client fixture pattern

Use FastAPI's `TestClient` against `app.main:app`:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

resp = client.get("/api/v1/healthz")
assert resp.status_code == 200
body = resp.json()
assert body["success"] is True
assert body["dev_code"] == "HEALTH_OK"
assert body["data"]["status"] == "ok"
assert "request_id" in body["metadata"]
```

## Envelope assertions

Prefer asserting on the envelope fields rather than raw payload shape only:

| Field | Why |
|-------|-----|
| `success` | Distinguishes business success from transport success |
| `status_code` | Mirrors HTTP status inside the body |
| `dev_code` | Stable machine-readable outcome for clients |
| `metadata.request_id` | Correlates with logs / `x-request-id` |

## Request ID coverage

```python
resp = client.get("/api/v1/healthz", headers={"X-Request-ID": "test-req-1"})
assert resp.headers["x-request-id"] == "test-req-1"
assert resp.json()["metadata"]["request_id"] == "test-req-1"
```

## CORS coverage

When `enableCors` is enabled at scaffold time, assert middleware is present:

```python
from app.main import app

assert any(m.cls.__name__ == "CORSMiddleware" for m in app.user_middleware)
```

## Tips

- Keep feature tests close to feature ownership; avoid a single mega-file.
- Prefer deterministic fixtures over sleeping / wall-clock waits.
- For database-backed features (via extensions), use per-test rollback sessions
  so examples stay hermetic.
