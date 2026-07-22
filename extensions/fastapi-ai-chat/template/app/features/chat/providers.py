"""LLM provider abstraction with a mock implementation for tests."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.features.chat.schemas import ChatMessage


class ChatProvider(ABC):
    name: str

    @abstractmethod
    def complete(self, messages: list[ChatMessage], model: str) -> ChatMessage:
        raise NotImplementedError


class MockChatProvider(ChatProvider):
    name = "mock"

    def complete(self, messages: list[ChatMessage], model: str) -> ChatMessage:
        last = messages[-1].content
        return ChatMessage(role="assistant", content=f"[mock:{model}] {last[::-1]}")


def get_provider(name: str) -> ChatProvider:
    if name == "mock":
        return MockChatProvider()
    # Future: openai, etc. — default to mock for safety in scaffolds
    return MockChatProvider()
