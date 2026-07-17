"""Typer entrypoint for the workspace CLI.

Demonstrates an app in ``apps/`` importing a library from ``packages/`` via the
uv workspace. Add commands with the ``@app.command()`` decorator.
"""

from __future__ import annotations

import typer

from core import greeting

app = typer.Typer(
    help="Workspace CLI powered by the shared core package.",
    no_args_is_help=True,
)


@app.callback()
def root() -> None:
    """Workspace CLI.

    Defining a callback keeps subcommands explicit even while there is only one,
    so adding more commands later does not change the invocation style.
    """


@app.command()
def hello(name: str = typer.Argument("world", help="Who to greet.")) -> None:
    """Print a greeting produced by the shared core library."""
    typer.echo(greeting(name))


def main() -> None:
    """Console-script entrypoint (see ``[project.scripts]``)."""
    app()


if __name__ == "__main__":
    main()
