"""CORS middleware registration tests."""

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.core.cors import setup_cors


def _middleware_types(app: FastAPI) -> list[type]:
    return [m.cls for m in app.user_middleware]


def test_no_middleware_when_origins_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    app = FastAPI()
    setup_cors(app)
    assert CORSMiddleware not in _middleware_types(app)


def test_no_middleware_when_origins_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "")
    app = FastAPI()
    setup_cors(app)
    assert CORSMiddleware not in _middleware_types(app)


def test_no_middleware_when_origins_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "  ,  ")
    app = FastAPI()
    setup_cors(app)
    assert CORSMiddleware not in _middleware_types(app)


def test_middleware_registered_with_single_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000")
    app = FastAPI()
    setup_cors(app)
    assert CORSMiddleware in _middleware_types(app)


def test_middleware_registered_with_multiple_origins(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    app = FastAPI()
    setup_cors(app)
    assert CORSMiddleware in _middleware_types(app)


def test_preflight_returns_allow_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    origin = "http://localhost:3000"
    monkeypatch.setenv("CORS_ORIGINS", origin)
    app = FastAPI()
    setup_cors(app)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.options(
        "/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == origin


def test_wildcard_origin_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "*")
    app = FastAPI()
    with pytest.raises(ValueError, match="Wildcard origin"):
        setup_cors(app)
