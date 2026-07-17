#!/usr/bin/env python3
"""L0 integrity: registry paths on disk + schema shape."""

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
        directory = template_dir(template)
        if not directory:
            errors.append(f"template {template.get('slug')}: cannot parse url")
            continue
        path = on_disk_path_for_entry("template", template)
        if path is None or not path.is_dir():
            errors.append(f"template {template.get('slug')}: missing on-disk path {path}")
        category = template.get("category")
        if category not in category_slugs:
            errors.append(f"template {template.get('slug')}: unknown category {category}")

    for extension in registry.get("extensions", []):
        directory = extension_dir(extension)
        if not directory:
            errors.append(f"extension {extension.get('slug')}: cannot parse url")
            continue
        path = on_disk_path_for_entry("extension", extension)
        if path is None or not path.is_dir():
            errors.append(f"extension {extension.get('slug')}: missing on-disk path {path}")
        category = extension.get("category")
        if category not in category_slugs:
            errors.append(f"extension {extension.get('slug')}: unknown category {category}")
        if not as_types(extension.get("type")):
            errors.append(f"extension {extension.get('slug')}: empty type")

        # Bidirectional incompatibleWith when declared
        for other_slug in extension.get("incompatibleWith") or []:
            other = next(
                (e for e in registry["extensions"] if e["slug"] == other_slug), None
            )
            if other is None:
                errors.append(
                    f"extension {extension['slug']}: incompatibleWith unknown slug {other_slug}"
                )
            elif extension["slug"] not in (other.get("incompatibleWith") or []):
                errors.append(
                    f"extension {extension['slug']}: incompatibleWith {other_slug} "
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
