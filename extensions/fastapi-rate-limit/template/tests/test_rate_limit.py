import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.core.rate_limit import limiter, setup_rate_limit


@pytest.fixture
def rate_limited_app() -> FastAPI:
    """Create a dummy application to test the rate limit extension wiring."""
    app = FastAPI()
    setup_rate_limit(app)

    # Use a low limit to easily trigger a 429
    @app.get("/test-limit")
    @limiter.limit("2/minute")
    async def test_endpoint(request: Request) -> dict[str, str]:
        return {"data": "ok"}

    return app


@pytest.fixture
def client(rate_limited_app: FastAPI) -> TestClient:
    return TestClient(rate_limited_app)


def test_rate_limit_enforcement(client: TestClient) -> None:
    """Test that requests exceeding the limit return a CPA-compliant 429 envelope."""
    # Request 1: Allowed
    resp1 = client.get("/test-limit")
    assert resp1.status_code == 200

    # Request 2: Allowed
    resp2 = client.get("/test-limit")
    assert resp2.status_code == 200

    # Request 3: Blocked
    resp3 = client.get("/test-limit")
    assert resp3.status_code == 429

    # Verify the CPA APIResponse envelope shape
    data = resp3.json()
    assert data["success"] is False
    assert data["dev_code"] == "RATE_LIMIT_EXCEEDED"
    assert "Rate limit exceeded" in data["message"]
