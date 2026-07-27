"""Chat service — env-driven settings, no external network calls in default path."""

from __future__ import annotations

import os

from fastapi import HTTPException, status
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from app.features.chat.providers import get_provider
from app.features.chat.schemas import ChatMessage, ChatRequest, ChatResponse

_ROLE_TO_MESSAGE: dict[str, type[BaseMessage]] = {
    "user": HumanMessage,
    "assistant": AIMessage,
    "system": SystemMessage,
}


def _max_input_chars() -> int:
    return int(os.environ.get("AI_CHAT_MAX_INPUT_CHARS", "4000"))


def _to_langchain_message(message: ChatMessage) -> BaseMessage:
    return _ROLE_TO_MESSAGE[message.role](content=message.content)


def chat_completion(body: ChatRequest) -> ChatResponse:
    total = sum(len(m.content) for m in body.messages)
    if total > _max_input_chars():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"input exceeds AI_CHAT_MAX_INPUT_CHARS ({_max_input_chars()})",
        )

    provider_name = os.environ.get("AI_CHAT_PROVIDER", "mock")
    model_name = body.model or os.environ.get("AI_CHAT_MODEL", "mock-chat")

    try:
        model = get_provider(provider_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc

    langchain_messages = [_to_langchain_message(m) for m in body.messages]
    ai_message = model.invoke(langchain_messages)

    return ChatResponse(
        message=ChatMessage(role="assistant", content=str(ai_message.content)),
        provider=provider_name,
        model=model_name,
    )
