"""Small LangGraph state graph: router → tool executor → responder.

Baseline orchestration, not a full agent framework. Routing is deterministic
(keyword-based) so the graph is testable offline with no LLM calls.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from app.features.agent_chat.tools import TOOL_REGISTRY
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class AgentChatState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    route: Literal["respond", "tool"]
    tool_name: str
    tool_args: dict[str, Any]
    tool_result: str


def _last_user_text(state: AgentChatState) -> str:
    for message in reversed(state.get("messages", [])):
        if isinstance(message, HumanMessage):
            return str(message.content)
    return ""


def router_node(state: AgentChatState) -> dict[str, Any]:
    """Pick the tool path for /tool commands, else respond directly."""
    text = _last_user_text(state).strip()
    if text.startswith("/time"):
        return {
            "route": "tool",
            "tool_name": "get_current_time",
            "tool_args": {},
        }
    if text.startswith("/echo "):
        return {
            "route": "tool",
            "tool_name": "echo_text",
            "tool_args": {"text": text[len("/echo ") :]},
        }
    return {"route": "respond"}


def tool_node(state: AgentChatState) -> dict[str, Any]:
    """Execute the registered tool selected by the router."""
    tool_name = state.get("tool_name", "")
    tool = TOOL_REGISTRY.get(tool_name)
    if tool is None:
        return {"tool_result": f"unknown tool: {tool_name}"}
    args = state.get("tool_args", {})
    try:
        return {"tool_result": str(tool(**args))}
    except TypeError as exc:
        return {"tool_result": f"tool {tool_name} failed: {exc}"}


def respond_node(state: AgentChatState) -> dict[str, Any]:
    """Compose the final assistant message (fake LLM baseline)."""
    tool_result = state.get("tool_result", "")
    if tool_result:
        content = f"[mock-agent:{state.get('route')}] tool result: {tool_result}"
    else:
        content = "[mock-agent:respond] Set AGENT_CHAT_PROVIDER to use a real model."
    return {"messages": [AIMessage(content=content)]}


def _route_after_router(state: AgentChatState) -> Literal["tool", "respond"]:
    return "tool" if state.get("route") == "tool" else "respond"


def build_agent_graph():
    """Compile the agent state graph."""
    graph = StateGraph(AgentChatState)
    graph.add_node("router", router_node)
    graph.add_node("tool", tool_node)
    graph.add_node("respond", respond_node)
    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", _route_after_router)
    graph.add_edge("tool", "respond")
    graph.add_edge("respond", END)
    return graph.compile()


agent_graph = build_agent_graph()
