#!/usr/bin/env python3
"""L0 integrity: registry paths, naming law, and template quality bar."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import (  # noqa: E402
    REPO_ROOT,
    TEMPLATES_JSON,
    as_types,
    extension_dir,
    load_registry,
    on_disk_path_for_entry,
    template_dir,
)

# Folder prefix required for stack-bound extensions (single type).
STACK_PREFIX_BY_TYPE: dict[str, str] = {
    "fastapi-backend": "fastapi",
    "django-backend": "django",
    "celery-worker": "celery",
    "cli-app": "cli",
    "uv-workspace": "uv-workspace",
    "mlops-sklearn": "mlops-sklearn",
}

REQUIRED_TEMPLATE_DOCS = (
    "docs/README.md",
    "docs/PROJECT_STRUCTURE.md",
    "docs/CONFIGURATION.md",
    "docs/TESTING_GUIDE.md",
    "docs/DEPLOYMENT.md",
    "docs/TYPING.md",
)

HTTP_API_TYPES = frozenset({"fastapi-backend", "django-backend"})


def _has_root_readme(path: Path) -> bool:
    return (path / "README.md").is_file() or (path / "README.md.template").is_file()


def _has_env_example(path: Path) -> bool:
    return (path / ".env.example").is_file() or (path / ".env.example.template").is_file()


def _has_agents_contributing(path: Path) -> bool:
    agents = (path / "AGENTS.md").is_file() or (path / "AGENTS.md.template").is_file()
    contrib = (path / "CONTRIBUTING.md").is_file() or (path / "CONTRIBUTING.md.template").is_file()
    return agents and contrib


def _has_tests(path: Path) -> bool:
    tests = path / "tests"
    if tests.is_dir():
        return any(tests.rglob("test_*.py")) or any(tests.rglob("test_*.py.template"))
    return any(
        p.is_dir()
        and p.name == "tests"
        and (any(p.rglob("test_*.py")) or any(p.rglob("test_*.py.template")))
        for p in path.rglob("tests")
    )


def validate_extension_folder_name(directory: str, types: list[str], slug: str) -> list[str]:
    errors: list[str] = []
    if directory.startswith("python-"):
        errors.append(
            f"extension {slug}: folder `{directory}` must not use deprecated python-* prefix"
        )
        return errors

    if directory.startswith("all-"):
        return errors

    if len(types) != 1:
        errors.append(
            f"extension {slug}: multi-type overlays must use all-* folder "
            f"(got `{directory}` for types={types})"
        )
        return errors

    prefix = STACK_PREFIX_BY_TYPE.get(types[0])
    if prefix is None:
        errors.append(
            f"extension {slug}: unknown type {types[0]!r} for stack folder check "
            f"(update STACK_PREFIX_BY_TYPE)"
        )
        return errors

    expected = f"{prefix}-"
    if not directory.startswith(expected):
        errors.append(
            f"extension {slug}: folder `{directory}` must be `all-*` or start with "
            f"`{expected}` for type {types[0]}"
        )
    return errors


def validate_template_quality_bar(slug: str, type_name: str, path: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_TEMPLATE_DOCS:
        if not (path / relative).is_file():
            errors.append(f"template {slug}: missing quality-bar file {relative}")

    if not _has_root_readme(path):
        errors.append(f"template {slug}: missing README.md or README.md.template")
    if not _has_agents_contributing(path):
        errors.append(f"template {slug}: missing AGENTS.md and/or CONTRIBUTING.md")
    if not _has_env_example(path):
        errors.append(f"template {slug}: missing .env.example or .env.example.template")
    if not _has_tests(path):
        errors.append(f"template {slug}: missing tests (test_*.py under tests/)")

    if type_name in HTTP_API_TYPES and not (path / "docs" / "API.md").is_file():
        errors.append(f"template {slug}: HTTP API templates require docs/API.md")

    return errors


def main() -> None:
    registry = load_registry()
    errors: list[str] = []

    if not TEMPLATES_JSON.is_file():
        errors.append(f"missing {TEMPLATES_JSON}")

    schema_path = REPO_ROOT / "templates.schema.json"
    if schema_path.is_file():
        json.loads(schema_path.read_text(encoding="utf-8"))

    category_slugs = {c["slug"] for c in registry.get("categories", [])}

    for template in registry.get("templates", []):
        slug = template.get("slug", "<unknown>")
        directory = template_dir(template)
        if not directory:
            errors.append(f"template {slug}: cannot parse url")
            continue
        path = on_disk_path_for_entry("template", template)
        if path is None or not path.is_dir():
            errors.append(f"template {slug}: missing on-disk path {path}")
            continue
        category = template.get("category")
        if category not in category_slugs:
            errors.append(f"template {slug}: unknown category {category}")
        type_name = template.get("type")
        if not isinstance(type_name, str) or not type_name:
            errors.append(f"template {slug}: missing string type")
        else:
            errors.extend(validate_template_quality_bar(slug, type_name, path))

    for extension in registry.get("extensions", []):
        slug = extension.get("slug", "<unknown>")
        directory = extension_dir(extension)
        if not directory:
            errors.append(f"extension {slug}: cannot parse url")
            continue
        path = on_disk_path_for_entry("extension", extension)
        if path is None or not path.is_dir():
            errors.append(f"extension {slug}: missing on-disk path {path}")
            continue
        category = extension.get("category")
        if category not in category_slugs:
            errors.append(f"extension {slug}: unknown category {category}")
        types = as_types(extension.get("type"))
        if not types:
            errors.append(f"extension {slug}: empty type")
        else:
            errors.extend(validate_extension_folder_name(directory, types, slug))

        for other_slug in extension.get("incompatibleWith") or []:
            other = next(
                (e for e in registry["extensions"] if e["slug"] == other_slug), None
            )
            if other is None:
                errors.append(
                    f"extension {slug}: incompatibleWith unknown slug {other_slug}"
                )
            elif slug not in (other.get("incompatibleWith") or []):
                errors.append(
                    f"extension {slug}: incompatibleWith {other_slug} "
                    "is not symmetric"
                )

    if errors:
        print("Registry integrity failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"✅ registry ok "
        f"({len(registry.get('templates', []))} templates, "
        f"{len(registry.get('extensions', []))} extensions)"
    )


if __name__ == "__main__":
    main()
