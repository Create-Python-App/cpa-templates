"""Agent chat service — runs the LangGraph orchestration offline by default."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from fastapi import HTTPException, status
from langchain_core.messages import BaseMessage, HumanMessage

from app.features.agent_chat.graph import agent_graph
from app.features.agent_chat.schemas import (
    AgentChatMessage,
    AgentChatRequest,
    AgentChatResponse,
)

try:  # AI span contract (#112): emit LLM spans when tracing is present.
    from app.core.mlflow_tracing import (  # type: ignore[import-untyped]
        maybe_start_span,
    )
except ImportError:  # fastapi-mlflow-tracing not applied → no-op span.

    @contextmanager
    def maybe_start_span(name: str, **attributes: Any) -> Generator[None, None, None]:
        yield None


_ROLE_TO_MESSAGE: dict[str, type[BaseMessage]] = {
    "user": HumanMessage,
}


def _max_input_chars() -> int:
    return int(os.environ.get("AGENT_CHAT_MAX_INPUT_CHARS", "4000"))


def agent_chat_completion(body: AgentChatRequest) -> AgentChatResponse:
    total = sum(len(m.content) for m in body.messages)
    limit = _max_input_chars()
    if total > limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"input exceeds AGENT_CHAT_MAX_INPUT_CHARS ({limit})",
        )

    provider_name = os.environ.get("AGENT_CHAT_PROVIDER", "mock")
    model_name = body.model or os.environ.get("AGENT_CHAT_MODEL", "mock-agent")
    if provider_name != "mock":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unknown AGENT_CHAT_PROVIDER: {provider_name!r} "
            "(only 'mock' is implemented in this MVP)",
        )

    langchain_messages: list[BaseMessage] = [
        HumanMessage(content=m.content) for m in body.messages if m.role == "user"
    ]
    if not langchain_messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="at least one user message is required",
        )

    with maybe_start_span(
        "agent_chat.completion", provider=provider_name, model=model_name
    ):
        final_state = agent_graph.invoke({"messages": langchain_messages})

    final_messages = final_state.get("messages", [])
    content = str(final_messages[-1].content) if final_messages else ""
    route = str(final_state.get("route", "respond"))
    return AgentChatResponse(
        message=AgentChatMessage(role="assistant", content=content),
        route=route,
        provider=provider_name,
        model=model_name,
    )
