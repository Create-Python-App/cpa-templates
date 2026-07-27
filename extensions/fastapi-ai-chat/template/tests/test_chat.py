"""Offline chat tests. No network calls, no real API keys."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.features.chat.providers import get_provider
from app.features.chat.router import router as chat_router
from app.features.chat.schemas import ChatMessage


def test_chat_message_accepts_valid_role() -> None:
    message = ChatMessage(role="user", content="hello")
    assert message.role == "user"
    assert message.content == "hello"


def test_chat_message_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError):
        ChatMessage(role="bogus", content="hello")


def test_chat_message_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        ChatMessage(role="user", content="")


def test_get_provider_mock_responds() -> None:
    provider = get_provider("mock")
    response = provider.invoke("hello")
    assert response.content == (
        "Hello! I'm a mock AI response. Set AI_CHAT_PROVIDER to use a real provider."
    )


def test_get_provider_mock_never_exhausts_across_calls() -> None:
    provider = get_provider("mock")
    first = provider.invoke("hello")
    second = provider.invoke("hello again")
    assert first.content == second.content


def test_get_provider_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="unknown AI_CHAT_PROVIDER"):
        get_provider("not-a-real-provider")


@pytest.fixture()
def client() -> TestClient:
    test_app = FastAPI()
    test_app.include_router(chat_router, prefix="/api/v1")
    return TestClient(test_app)


def test_chat_mock_roundtrip(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_CHAT_PROVIDER", "mock")
    response = client.post(
        "/api/v1/chat",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["dev_code"] == "CHAT_COMPLETED"
    message = body["data"]["message"]
    assert message["role"] == "assistant"
    assert message["content"]
    assert body["data"]["provider"] == "mock"


def test_chat_rejects_oversized_input(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_CHAT_MAX_INPUT_CHARS", "5")
    response = client.post(
        "/api/v1/chat",
        json={"messages": [{"role": "user", "content": "too-long-input"}]},
    )
    assert response.status_code == 400


def test_chat_rejects_unknown_provider(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_CHAT_PROVIDER", "not-a-real-provider")
    response = client.post(
        "/api/v1/chat",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 500
