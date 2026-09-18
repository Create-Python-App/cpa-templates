"""Tests for the FastAPI MCP client extension (generated project)."""

from __future__ import annotations

import os
import tempfile
from typing import Annotated

import yaml  # type: ignore[import-untyped]
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.core.mcp_client import MCPClient


def test_mcp_client_initialization() -> None:
    client = MCPClient()
    assert client is not None
    assert hasattr(client, "list_tools")
    assert hasattr(client, "execute_tool")


def test_mcp_client_from_env() -> None:
    client = MCPClient.from_env()
    assert client is not None


def test_mcp_client_yaml_config() -> None:
    config = {
        "servers": [
            {
                "name": "test-server",
                "type": "stdio",
                "command": "echo",
                "args": ["test"],
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name

    try:
        client = MCPClient.from_yaml(config_path)
        assert client is not None
        assert hasattr(client, "config")
    finally:
        os.unlink(config_path)


def _no_mcp() -> MCPClient | None:
    return None


def test_fastapi_integration() -> None:
    app = FastAPI()

    @app.get("/mcp-tools")
    async def list_tools(mcp: Annotated[MCPClient | None, Depends(_no_mcp)]):
        if mcp:
            return {"tools": await mcp.list_tools()}
        return {"tools": []}

    client = TestClient(app)
    response = client.get("/mcp-tools")
    assert response.status_code == 200
    assert "tools" in response.json()
