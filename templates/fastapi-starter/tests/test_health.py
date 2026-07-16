"""Health endpoint tests."""

from fastapi.testclient import TestClient


def test_healthz_returns_healthy(client: TestClient) -> None:
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "fastapi-starter"
    assert "timestamp" in body


def test_ping_returns_ok(client: TestClient) -> None:
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
