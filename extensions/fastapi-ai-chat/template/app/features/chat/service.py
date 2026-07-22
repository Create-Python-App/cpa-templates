"""Chat service — env-driven settings, no external network calls in default path."""

from __future__ import annotations

import os

from fastapi import HTTPException, status

from app.features.chat.providers import get_provider
from app.features.chat.schemas import ChatRequest, ChatResponse


def _max_input_chars() -> int:
    return int(os.environ.get("AI_CHAT_MAX_INPUT_CHARS", "4000"))


def chat_completion(body: ChatRequest) -> ChatResponse:
    total = sum(len(m.content) for m in body.messages)
    if total > _max_input_chars():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"input exceeds AI_CHAT_MAX_INPUT_CHARS ({_max_input_chars()})",
        )
    provider_name = os.environ.get("AI_CHAT_PROVIDER", "mock")
    model = body.model or os.environ.get("AI_CHAT_MODEL", "mock-chat")
    provider = get_provider(provider_name)
    message = provider.complete(body.messages, model)
    return ChatResponse(message=message, provider=provider.name, model=model)
