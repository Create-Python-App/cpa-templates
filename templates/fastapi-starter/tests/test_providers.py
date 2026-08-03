"""Tests for the app provider registry."""

from __future__ import annotations

from fastapi import FastAPI

from app.core.providers import _providers, register, setup_app


def _make_app() -> FastAPI:
    return FastAPI()


def test_register_appends_to_providers() -> None:
    initial_count = len(_providers)

    def noop(app: FastAPI) -> None:
        pass

    register(noop)
    assert len(_providers) == initial_count + 1
    _providers.remove(noop)


def test_register_returns_the_function() -> None:
    def noop(app: FastAPI) -> None:
        pass

    result = register(noop)
    assert result is noop
    _providers.remove(noop)


def test_setup_app_calls_all_providers_in_order() -> None:
    app = _make_app()
    calls: list[str] = []

    def first(a: FastAPI) -> None:
        calls.append("first")

    def second(a: FastAPI) -> None:
        calls.append("second")

    _providers.extend([first, second])
    try:
        setup_app(app)
    finally:
        _providers.remove(first)
        _providers.remove(second)

    assert calls == ["first", "second"]


def test_setup_app_empty_registry_is_noop() -> None:
    saved = _providers[:]
    _providers.clear()
    try:
        setup_app(_make_app())  # must not raise
    finally:
        _providers.extend(saved)
