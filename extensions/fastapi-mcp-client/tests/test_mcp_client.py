"""Tests for FastAPI MCP Client extension."""
import pytest
from fastapi_mcp_client import MCPClient
from fastapi.testclient import TestClient
from fastapi import FastAPI


def test_mcp_client_initialization():
    """Test MCPClient initialization."""
    client = MCPClient()
    assert client is not None
    assert hasattr(client, 'list_tools')
    assert hasattr(client, 'execute_tool')


def test_mcp_client_from_env():
    """Test MCPClient initialization from environment."""
    client = MCPClient.from_env()
    assert client is not None


def test_mcp_client_yaml_config():
    """Test MCPClient initialization from YAML config."""
    import tempfile
    import yaml
    
    config = {
        'servers': [
            {
                'name': 'test-server',
                'type': 'stdio',
                'command': 'echo',
                'args': ['test']
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name
    
    try:
        client = MCPClient.from_yaml(config_path)
        assert client is not None
        assert hasattr(client, 'config')
    finally:
        import os
        os.unlink(config_path)


def test_fastapi_integration():
    """Test FastAPI integration with MCP client."""
    app = FastAPI()
    
    @app.get("/mcp-tools")
    async def list_tools(mcp: MCPClient = None):
        if mcp:
            return {"tools": await mcp.list_tools()}
        return {"tools": []}
    
    client = TestClient(app)
    response = client.get("/mcp-tools")
    assert response.status_code == 200
    assert "tools" in response.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])