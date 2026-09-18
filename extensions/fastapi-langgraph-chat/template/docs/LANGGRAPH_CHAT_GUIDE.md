# LangGraph Chat Guide

## Overview

The **fastapi-langgraph-chat** extension adds a multi-step agent endpoint
(`POST /agent/chat`) layered on a FastAPI app. A small LangGraph state graph
routes each request — `router → tool → responder` — with a mock toolset so it
works offline with no API key. It intentionally does not include RAG, MCP, or
MLflow tracing; those are optional follow-up extensions.

The route (`/agent/chat`) does not conflict with `fastapi-ai-chat` (`/chat`);
both extensions can be applied together with no `incompatibleWith` entry.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `langgraph` + `langchain-core` |
| `app/features/agent_chat/schemas.py` | `AgentChatMessage`, `AgentChatRequest`, `AgentChatResponse` |
| `app/features/agent_chat/tools.py` | `TOOL_REGISTRY` of typed native tools |
| `app/features/agent_chat/graph.py` | Typed state + router/tool/responder nodes, compiled graph |
| `app/features/agent_chat/service.py` | Input validation, graph invocation, span emission |
| `app/features/agent_chat/router.py` | `POST /agent/chat` |
| `app/api/router.py.append` | Auto-mounts the agent router |
| `tests/test_agent_chat.py` | Offline graph + endpoint tests |
| `.env.example.append` | `AGENT_CHAT_*` placeholders |

## How it works

`router_node` inspects the last user message: `/time` and `/echo <text>`
take the tool path, everything else responds directly. `tool_node` executes
the registered tool; `respond_node` composes the final assistant message,
including the tool result when present. When `fastapi-mlflow-tracing` is also
applied, the service emits a `agent_chat.completion` span (AI span contract).

## Call the endpoint

```sh
curl -s -X POST http://localhost:8000/api/v1/agent/chat \
  -H 'content-type: application/json' \
  -d '{"messages": [{"role": "user", "content": "/echo hi"}]}'
```

## Add a new node or tool safely

1. **Tool**: define a typed function in `tools.py` and register it in
   `TOOL_REGISTRY`. Add a routing rule in `router_node` and cover both in
   `tests/test_agent_chat.py`.
2. **Node**: add the function in `graph.py`, register it with
   `graph.add_node`, and wire edges explicitly. Keep nodes pure functions of
   state returning partial state updates.
3. Never call external LLMs from nodes in the default path — keep the mock
   provider so tests stay offline.
