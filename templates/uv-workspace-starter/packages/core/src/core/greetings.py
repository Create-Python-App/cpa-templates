"""Tiny demo library consumed by workspace apps.

Replace this with your real shared logic. It exists to show how an app in
``apps/`` depends on a library in ``packages/`` through the uv workspace.
"""

from __future__ import annotations


def greeting(name: str) -> str:
    """Return a friendly greeting for ``name`` (falls back to ``world``)."""
    cleaned = name.strip() or "world"
    return f"Hello, {cleaned}!"
