#!/usr/bin/env python3
"""Generate GitHub Actions matrices for layered CI (see #46)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from registry import (  # noqa: E402
    REPO_ROOT,
    as_types,
    assert_profile_valid,
    canonical_template_dir_for_type,
    extension_dir,
    extension_file_url,
    find_template_by_dir,
    load_profiles,
    load_registry,
    template_dir,
    template_file_url,
)


def changed_paths(base_ref: str) -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
            cwd=REPO_ROOT,
            text=True,
        )
        return [line.strip() for line in out.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        # Fail closed: treat as "everything changed" so PR CI does not go green
        # with an empty matrix when git history is shallow/broken.
        print(
            f"⚠ git diff {base_ref}...HEAD failed — forcing full matrix",
            file=sys.stderr,
        )
        return ["templates.json"]


def force_full_matrix(changed: list[str]) -> bool:
    triggers = (
        "templates.json",
        "scripts/ci/",
        "ci/profiles/",
        ".github/workflows/ci-",
    )
    return any(path == t or path.startswith(t) for path in changed for t in triggers)


def matrix_templates(registry: dict) -> list[dict]:
    cells = []
    for template in registry["templates"]:
        directory = template_dir(template)
        cells.append(
            {
                "id": f"L1 · {directory}",
                "slug": template["slug"],
                "templateDir": directory,
                "templateUrl": template_file_url(REPO_ROOT, template),
                "addons": [],
            }
        )
    return cells


def matrix_extensions(registry: dict, changed_only: bool, base_ref: str) -> list[dict]:
    changed = changed_paths(base_ref) if changed_only else []
    full = (not changed_only) or force_full_matrix(changed)
    changed_ext_dirs = {
        path.split("/")[1]
        for path in changed
        if path.startswith("extensions/") and len(path.split("/")) > 1
    }

    cells: list[dict] = []
    seen: set[str] = set()
    missing_canonical: list[str] = []

    for extension in registry["extensions"]:
        directory = extension_dir(extension)
        if not full and directory not in changed_ext_dirs:
            continue

        for type_name in as_types(extension.get("type")):
            canonical_dir = canonical_template_dir_for_type(type_name)
            if not canonical_dir:
                missing_canonical.append(f"{extension['slug']} type={type_name}")
                continue
            template = find_template_by_dir(registry, canonical_dir)
            if not template:
                missing_canonical.append(
                    f"{extension['slug']} type={type_name} → missing {canonical_dir}"
                )
                continue

            key = f"{extension['slug']}@@{canonical_dir}"
            if key in seen:
                continue
            seen.add(key)

            cells.append(
                {
                    "id": f"L2 · {extension['slug']} @ {canonical_dir}",
                    "slug": extension["slug"],
                    "extensionDir": directory,
                    "templateDir": canonical_dir,
                    "templateUrl": template_file_url(REPO_ROOT, template),
                    "addons": [extension_file_url(REPO_ROOT, extension)],
                    "type": type_name,
                }
            )

    if missing_canonical:
        raise SystemExit(
            "Extensions without a canonical L2 template:\n  - "
            + "\n  - ".join(missing_canonical)
        )
    return cells


def matrix_profiles(registry: dict, changed_only: bool, base_ref: str) -> list[dict]:
    profiles = load_profiles()
    changed = changed_paths(base_ref) if changed_only else []
    full = (not changed_only) or force_full_matrix(changed)

    cells: list[dict] = []
    for profile in profiles:
        template, addons = assert_profile_valid(registry, profile)

        if not full:
            touched_template = any(
                path.startswith(f"templates/{profile['templateDir']}/") for path in changed
            )
            touched_addon = any(
                any(
                    path.startswith(f"extensions/{extension_dir(ext)}/")
                    for path in changed
                )
                for ext in addons
            )
            touched_profile = any(
                path == f"ci/profiles/{profile['_file']}" for path in changed
            )
            if not (touched_template or touched_addon or touched_profile):
                continue

        cells.append(
            {
                "id": f"L3 · {profile['id']}",
                "profileId": profile["id"],
                "templateDir": profile["templateDir"],
                "templateUrl": template_file_url(REPO_ROOT, template),
                "addons": [extension_file_url(REPO_ROOT, ext) for ext in addons],
                "sets": profile.get("sets") or {},
            }
        )
    return cells


def validate_all_profiles(registry: dict) -> list[dict]:
    profiles = load_profiles()
    for profile in profiles:
        assert_profile_valid(registry, profile)
        print(f"✅ profile {profile['id']}", file=sys.stderr)
    print(f"Validated {len(profiles)} profiles", file=sys.stderr)
    return []


def write_output(matrix: list[dict]) -> None:
    payload = json.dumps(matrix)
    sys.stdout.write(payload + "\n")
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        delim = "MATRIX_EOF"
        with Path(github_output).open("a", encoding="utf-8") as handle:
            handle.write(f"matrix<<{delim}\n{payload}\n{delim}\n")
            handle.write(f"count={len(matrix)}\n")
    print(f"Generated {len(matrix)} matrix cell(s)", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate layered CI matrices for cpa-templates"
    )
    parser.add_argument(
        "--layer",
        required=True,
        choices=["templates", "extensions", "profiles", "validate-profiles"],
    )
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()

    registry = load_registry()
    if args.layer == "templates":
        matrix = matrix_templates(registry)
    elif args.layer == "extensions":
        matrix = matrix_extensions(registry, args.changed_only, args.base_ref)
    elif args.layer == "profiles":
        matrix = matrix_profiles(registry, args.changed_only, args.base_ref)
    else:
        matrix = validate_all_profiles(registry)

    write_output(matrix)


if __name__ == "__main__":
    main()
