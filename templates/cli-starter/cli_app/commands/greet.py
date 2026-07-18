"""Greeting command implementation."""

from __future__ import annotations

from rich.console import Console

console = Console()


def hello(name: str = "world") -> None:
    """Print a friendly greeting."""
    console.print(f"Hello, {name}!")
