"""Typer entrypoint for the CLI starter."""

from __future__ import annotations

import typer
from rich.console import Console

from cli_app import __version__

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
    if version:
        console.print(__version__)
        raise typer.Exit(0)
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


@app.command()
def hello(name: str = typer.Argument("world", help="Who to greet.")) -> None:
    """Print a friendly greeting."""
    console.print(f"Hello, {name}!")
