import re

from typer.testing import CliRunner

from cli_app.cli import app

runner = CliRunner()
_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _plain(text: str) -> str:
    return _ANSI.sub("", text)


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in _plain(result.stdout)


def test_hello_default() -> None:
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, world!" in _plain(result.stdout)


def test_hello_name() -> None:
    result = runner.invoke(app, ["hello", "CPA"])
    assert result.exit_code == 0
    assert "Hello, CPA!" in _plain(result.stdout)


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in _plain(result.stdout)
