# fastapi-mcp-client

A FastAPI extension for composing MCP tools and skills in AI applications.

## Overview

This extension provides a client for the Model Context Protocol (MCP) that can be composed with FastAPI applications to leverage external tools and capabilities.

## Features

- **MCP client configuration**: Manage MCP servers and tool registration
- **Tool registry**: Typed service for discovering and using MCP tools
- **Integration points**: Easy composition with FastAPI AI apps
- **Environment-based configuration**: Support for `mcp_servers.yaml` or env-driven setup

## Usage

Add the extension to your FastAPI application:

```python
from fastapi import FastAPI
from fastapi_mcp_client import MCPClient

app = FastAPI()

# Initialize MCP client
mcp_client = MCPClient.from_env()

@app.get("/tools")
async def list_tools():
    return {"tools": await mcp_client.list_tools()}

@app.post("/tool/{tool_name}")
async def execute_tool(tool_name: str, parameters: dict):
    return await mcp_client.execute_tool(tool_name, parameters)
```

## Configuration

### Environment Variables

```env
MCP_SERVERS_FILE=/path/to/mcp_servers.yaml
MCP_CLIENT_ENABLED=true
```

### mcp_servers.yaml Example

```yaml
servers:
  - name: "weather-api"
    type: "stdio"
    command: "python"
    args: ["weather_server.py"]
    env:
      API_KEY: "${WEATHER_API_KEY}"
```

## Testing

Run the test suite:

```bash
pytest extensions/fastapi-mcp-client/tests/test_mcp_client.py -v
```

## License

MIT