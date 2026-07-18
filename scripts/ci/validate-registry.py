#!/usr/bin/env python3
"""L0 integrity: registry paths on disk + schema shape + extension naming law."""

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
}


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


def main() -> None:
    registry = load_registry()
    errors: list[str] = []

    if not TEMPLATES_JSON.is_file():
        errors.append(f"missing {TEMPLATES_JSON}")

    schema_path = REPO_ROOT / "templates.schema.json"
    if schema_path.is_file():
        # Structural presence only; full JSON Schema validation is optional.
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

        # Bidirectional incompatibleWith when declared
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
