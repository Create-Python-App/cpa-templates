"""Typer entrypoint for the CLI starter."""

from __future__ import annotations

import logging

import typer
from rich.console import Console

from cli_app import __version__
from cli_app.commands import greet, info
from cli_app.config import load_settings

app = typer.Typer(
    name="cli",
    help="CLI starter scaffolded with create-awesome-python-app.",
    no_args_is_help=True,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    settings = load_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
    ctx.ensure_object(dict)
    ctx.obj["settings"] = settings

    if version:
        console.print(__version__)
        raise typer.Exit(0)
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@app.command("hello")
def hello_cmd(name: str = typer.Argument("world", help="Who to greet.")) -> None:
    """Print a friendly greeting."""
    greet.hello(name)


@app.command("version")
def version_cmd() -> None:
    """Print the package version (same as --version)."""
    info.show_version()
