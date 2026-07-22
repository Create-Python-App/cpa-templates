#!/usr/bin/env python3
"""Scaffold a template (+ optional addons) via uvx from PyPI and run health checks.

Hard constraint (#46): always invoke the published CLI with `uvx create-awesome-python-app`.
Never check out create-python-app source. Never fall back to a local install.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import REPO_ROOT  # noqa: E402

CLI_PACKAGE = "create-awesome-python-app"
# Pin to the published distribution channel users get; `@latest` refreshes on runners.
UVX_SPEC = f"{CLI_PACKAGE}@latest"


def fail(phase: str, message: str, code: int = 1) -> None:
    print(f"\n❌ [{phase}] {message}", file=sys.stderr)
    raise SystemExit(code)


def run(phase: str, cmd: list[str], *, cwd: Path | None = None, env: dict | None = None) -> None:
    print(f"\n▶ [{phase}] {' '.join(cmd)}")
    merged = {
        **os.environ,
        "CI": "true",
        "CPA_SKIP_GIT": os.environ.get("CPA_SKIP_GIT", "1"),
        "FORCE_COLOR": "0",
        **(env or {}),
    }
    result = subprocess.run(cmd, cwd=cwd, env=merged)
    if result.returncode != 0:
        fail(phase, f"command failed with exit code {result.returncode}", result.returncode)


def resolve_file_target(file_url: str) -> Path:
    if not file_url.startswith("file://"):
        fail("scaffold", f"URL must be file://, got: {file_url}")
    parsed = urlparse(file_url)
    pathname = unquote(parsed.path)
    subdir_list = parse_qs(parsed.query).get("subdir")
    if subdir_list:
        return Path(pathname) / subdir_list[0]
    return Path(pathname)


def assert_template_url_exists(template_url: str) -> None:
    target = resolve_file_target(template_url)
    if not target.exists():
        fail(
            "scaffold",
            f"template path does not exist: {target}\n"
            "  (refusing to continue — this is how empty scaffolds go green)",
        )
    if not target.is_dir():
        fail("scaffold", f"template path is not a directory: {target}")
    print(f"✅ [scaffold] template path exists: {target}")


def assert_non_empty_project(project_root: Path) -> None:
    pyproject = project_root / "pyproject.toml"
    if not pyproject.is_file():
        fail("empty-guard", f"missing pyproject.toml in {project_root}")

    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = data.get("project") or {}
    deps = list(project.get("dependencies") or [])
    groups = data.get("dependency-groups") or {}
    group_dep_count = sum(len(v) for v in groups.values() if isinstance(v, list))
    dep_count = len(deps) + group_dep_count

    entries = [
        name
        for name in os.listdir(project_root)
        if name not in {".git", ".venv", ".ci-meta.json", "__pycache__"}
    ]

    if len(entries) < 3 and dep_count == 0:
        fail(
            "empty-guard",
            f"scaffold looks empty ({len(entries)} entries, 0 deps). "
            "Likely wrong template path / silent no-op copy.",
        )

    if dep_count == 0:
        fail(
            "empty-guard",
            "pyproject.toml has no dependencies / dependency-groups — refusing green CI",
        )

    print(
        f"✅ [empty-guard] project ok ({len(entries)} top-level entries, {dep_count} deps)"
    )


def has_tool_config(project_root: Path, tool: str) -> bool:
    pyproject = project_root / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    tools = data.get("tool") or {}
    if tool in tools:
        return True
    groups = data.get("dependency-groups") or {}
    for group_deps in groups.values():
        if not isinstance(group_deps, list):
            continue
        for dep in group_deps:
            if isinstance(dep, str) and dep.split(">")[0].split("=")[0].split("[")[0] == tool:
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="CPA layered CI scaffold check (uvx/PyPI only)")
    parser.add_argument("--template-url", required=True)
    parser.add_argument("--addon-url", action="append", default=[])
    parser.add_argument("--set", dest="sets", action="append", default=[])
    parser.add_argument("--workdir", default=str(REPO_ROOT / ".ci-scaffold"))
    parser.add_argument("--project-name", default="scaffold-check")
    parser.add_argument("--skip-test", action="store_true")
    parser.add_argument("--skip-lint", action="store_true")
    parser.add_argument("--skip-type-check", action="store_true")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    for assignment in args.sets:
        if assignment.startswith("projectName="):
            args.project_name = assignment.split("=", 1)[1]

    if shutil.which("uvx") is None:
        fail("scaffold", "uvx not found on PATH — install uv (https://docs.astral.sh/uv/)")

    assert_template_url_exists(args.template_url)

    workdir = Path(args.workdir)
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)

    project_root = workdir / args.project_name

    # Put project_directory before options. Published CLI 0.2.10's argv expander
    # treats --template URL values as "saw_positional", so a trailing directory
    # after --addons is incorrectly kept as another addon (Invalid catalog slug).
    scaffold_cmd = [
        "uvx",
        UVX_SPEC,
        args.project_name,
        "--template",
        args.template_url,
        "--no-interactive",
        "--no-install",
    ]
    # Typer list options take one value per flag. Passing multiple URLs after a
    # single --addons makes later URLs look like project_directory / COMMAND.
    for addon_url in args.addon_url:
        scaffold_cmd.extend(["--addons", addon_url])
    for assignment in args.sets:
        scaffold_cmd.extend(["--set", assignment])

    run("scaffold", scaffold_cmd, cwd=workdir)

    if not project_root.is_dir():
        fail("scaffold", f"expected project at {project_root}")

    assert_non_empty_project(project_root)

    run("install", ["uv", "sync"], cwd=project_root)

    if not args.skip_lint and has_tool_config(project_root, "ruff"):
        run("lint", ["uv", "run", "ruff", "check", "."], cwd=project_root)
    elif not args.skip_lint:
        print("ℹ [lint] skipped (ruff not configured)")

    if not args.skip_type_check:
        if has_tool_config(project_root, "mypy"):
            run("type-check", ["uv", "run", "mypy", "."], cwd=project_root)
        if has_tool_config(project_root, "pyright"):
            run("type-check", ["uv", "run", "pyright"], cwd=project_root)

    if not args.skip_test:
        if has_tool_config(project_root, "pytest") or (project_root / "tests").is_dir():
            run("test", ["uv", "run", "pytest", "-q"], cwd=project_root)
        else:
            print("ℹ [test] skipped (no pytest / tests/)")

    print("\n✅ scaffold-check passed")
    if not args.keep:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
