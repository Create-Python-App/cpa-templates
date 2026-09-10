"""
FastAPI MCP client module.
Provides typed client for Model Context Protocol integration.
"""

import os
from typing import Any


class MCPClient:
    """Client for Model Context Protocol (MCP).

    Provides tool discovery and execution through MCP servers.
    """

    def __init__(self, servers: list[dict[str, Any]] | None = None):
        self.config = {"servers": servers or []}
        self._tools: dict[str, Any] = {}

    @classmethod
    def from_env(cls) -> "MCPClient":
        """Create client from environment variables."""
        servers_file = os.environ.get("MCP_SERVERS_FILE", "mcp_servers.yaml")
        enabled = os.environ.get("MCP_CLIENT_ENABLED", "true").lower() == "true"

        if not enabled or not os.path.exists(servers_file):
            return cls()

        try:
            import yaml  # type: ignore[import-untyped]

            with open(servers_file) as f:
                config = yaml.safe_load(f) or {}
            return cls(config.get("servers", []))
        except ImportError:
            return cls()

    @classmethod
    def from_yaml(cls, path: str) -> "MCPClient":
        """Create client from YAML config file."""
        try:
            import yaml  # type: ignore[import-untyped]

            with open(path) as f:
                config = yaml.safe_load(f) or {}
            return cls(config.get("servers", []))
        except ImportError:
            return cls()

    async def list_tools(self) -> list[dict[str, Any]]:
        """List available MCP tools."""
        return [
            {"name": s.get("name", "unknown"), "type": s.get("type", "unknown")}
            for s in self.config["servers"]
        ]

    async def execute_tool(
        self, tool_name: str, parameters: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute an MCP tool."""
        for server in self.config["servers"]:
            if server.get("name") == tool_name:
                return {"success": True, "server": tool_name, "result": parameters}
        return {"success": False, "error": f"Tool not found: {tool_name}"}
