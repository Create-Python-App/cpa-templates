"""Offline agent chat tests. No network calls, no real API keys."""

import pytest
from app.features.agent_chat.graph import agent_graph, router_node, tool_node
from app.features.agent_chat.router import router as agent_chat_router
from app.features.agent_chat.schemas import AgentChatMessage
from app.features.agent_chat.tools import TOOL_REGISTRY
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError


def test_agent_message_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError):
        AgentChatMessage(role="bogus", content="hello")


def test_router_routes_tool_commands() -> None:
    from langchain_core.messages import HumanMessage

    state = router_node({"messages": [HumanMessage(content="/time")]})
    assert state["route"] == "tool"
    assert state["tool_name"] == "get_current_time"

    state = router_node({"messages": [HumanMessage(content="/echo hi")]})
    assert state["route"] == "tool"
    assert state["tool_args"] == {"text": "hi"}


def test_router_defaults_to_respond() -> None:
    from langchain_core.messages import HumanMessage

    state = router_node({"messages": [HumanMessage(content="hello")]})
    assert state["route"] == "respond"


def test_tool_node_executes_registered_tool() -> None:
    result = tool_node({"tool_name": "echo_text", "tool_args": {"text": "hi"}})
    assert result == {"tool_result": "hi"}


def test_tool_node_reports_unknown_tool() -> None:
    result = tool_node({"tool_name": "nope", "tool_args": {}})
    assert result == {"tool_result": "unknown tool: nope"}


def test_every_registered_tool_runs_offline() -> None:
    assert set(TOOL_REGISTRY) == {"get_current_time", "echo_text"}
    assert TOOL_REGISTRY["get_current_time"]()
    assert TOOL_REGISTRY["echo_text"]("x") == "x"


def test_graph_tool_path_builds_final_response() -> None:
    from langchain_core.messages import HumanMessage

    final = agent_graph.invoke({"messages": [HumanMessage(content="/echo hi")]})
    assert final["route"] == "tool"
    assert "hi" in str(final["messages"][-1].content)


def test_graph_respond_path_builds_final_response() -> None:
    from langchain_core.messages import HumanMessage

    final = agent_graph.invoke({"messages": [HumanMessage(content="hello")]})
    assert final["route"] == "respond"
    assert "mock-agent" in str(final["messages"][-1].content)


@pytest.fixture()
def client() -> TestClient:
    test_app = FastAPI()
    test_app.include_router(agent_chat_router, prefix="/api/v1")
    return TestClient(test_app)


def test_agent_chat_roundtrip(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AGENT_CHAT_PROVIDER", "mock")
    response = client.post(
        "/api/v1/agent/chat",
        json={"messages": [{"role": "user", "content": "/echo hi"}]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["dev_code"] == "AGENT_CHAT_COMPLETED"
    assert body["data"]["route"] == "tool"
    assert "hi" in body["data"]["message"]["content"]


def test_agent_chat_rejects_oversized_input(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AGENT_CHAT_MAX_INPUT_CHARS", "5")
    response = client.post(
        "/api/v1/agent/chat",
        json={"messages": [{"role": "user", "content": "too-long-input"}]},
    )
    assert response.status_code == 400
