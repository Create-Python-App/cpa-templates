"""Native tools for the agent graph — typed plain functions.

Add a tool by defining a function with typed parameters and registering it
in ``TOOL_REGISTRY``. Keep tools dependency-free and offline-safe; the graph
test suite calls every registered tool.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime


def get_current_time() -> str:
    """Current UTC time as an ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def echo_text(text: str) -> str:
    """Echo back the caller's text (smoke-test tool)."""
    return text


TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "get_current_time": get_current_time,
    "echo_text": echo_text,
}
