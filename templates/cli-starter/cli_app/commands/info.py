"""Informational command implementations."""

from __future__ import annotations

from rich.console import Console

from cli_app import __version__

console = Console()


def show_version() -> None:
    """Print the package version."""
    console.print(__version__)
