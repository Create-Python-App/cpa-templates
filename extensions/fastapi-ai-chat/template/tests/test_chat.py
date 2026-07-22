"""Offline chat tests using the mock provider."""

import os

import pytest
from fastapi.testclient import TestClient

# Ensure mock provider before app import side effects
os.environ.setdefault("AI_CHAT_PROVIDER", "mock")


@pytest.fixture()
def client():
    from app.main import app

    return TestClient(app)


def test_chat_mock_roundtrip(client) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 200
    data = response.json()
    # APIResponse wrapper or raw — support both
    payload = data.get("data", data)
    message = payload.get("message", payload)
    assert message["role"] == "assistant"
    assert "olleh" in message["content"]


def test_chat_rejects_oversized_input(client, monkeypatch) -> None:
    monkeypatch.setenv("AI_CHAT_MAX_INPUT_CHARS", "5")
    response = client.post(
        "/api/v1/chat",
        json={"messages": [{"role": "user", "content": "too-long-input"}]},
    )
    assert response.status_code == 400
