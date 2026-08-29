# MCP Client Guide

Guide for using the MCP client extension with FastAPI.

## Overview

The MCP (Model Context Protocol) client extension provides a way to integrate external tools and services into your FastAPI AI application.

## Configuration

### Environment Variables

```env
MCP_SERVERS_FILE=mcp_servers.yaml
MCP_CLIENT_ENABLED=true
```

### mcp_servers.yaml

```yaml
servers:
  - name: "weather-api"
    type: "stdio"
    command: "python"
    args: ["weather_server.py"]
```

## Usage

```python
from fastapi import FastAPI
from fastapi_mcp_client import MCPClient

app = FastAPI()

mcp = MCPClient.from_env()

@app.get("/tools")
async def list_tools():
    return await mcp.list_tools()
```

## Adding Tools

Define MCP tools in your `mcp_servers.yaml` and they'll be automatically discovered and made available through the client.