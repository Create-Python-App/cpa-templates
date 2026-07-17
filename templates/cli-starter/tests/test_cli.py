from typer.testing import CliRunner

from cli_app.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_hello_default() -> None:
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, world!" in result.stdout


def test_hello_name() -> None:
    result = runner.invoke(app, ["hello", "CPA"])
    assert result.exit_code == 0
    assert "Hello, CPA!" in result.stdout
