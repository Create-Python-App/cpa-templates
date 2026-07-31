#!/usr/bin/env python3
"""Registry helpers for layered CI (see #46)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_JSON = REPO_ROOT / "templates.json"
PROFILES_DIR = REPO_ROOT / "ci" / "profiles"

# Canonical template directory per extension `type`.
CANONICAL_TEMPLATE_BY_TYPE: dict[str, str] = {
    "fastapi-backend": "fastapi-starter",
    "django-backend": "django-api",
    "cli-app": "cli-starter",
    "celery-worker": "celery-worker",
    "uv-workspace": "uv-workspace-starter",
    "mlops-sklearn": "mlops-sklearn-starter",
}


def load_registry() -> dict[str, Any]:
    return json.loads(TEMPLATES_JSON.read_text(encoding="utf-8"))


def dir_from_url(url: str, kind: str) -> str | None:
    """Resolve on-disk directory name from a registry URL.

    CPA registry URLs look like:
      https://github.com/Create-Python-App/cpa-templates?subdir=templates/fastapi-starter
    (subdir lives in the query string, not the path).
    """
    prefix = "templates" if kind == "template" else "extensions"
    # Query-string form (canonical for CPA)
    match = re.search(rf"[?&]subdir={prefix}/([^/&]+)(?:/|&|$)", url or "")
    if match:
        return match.group(1)
    # Path form (compat)
    match = re.search(rf"/{prefix}/([^/]+)(?:/|$)", url or "")
    return match.group(1) if match else None


def template_dir(template: dict[str, Any]) -> str | None:
    return dir_from_url(template.get("url", ""), "template")


def extension_dir(extension: dict[str, Any]) -> str | None:
    return dir_from_url(extension.get("url", ""), "extension")


def as_types(type_field: Any) -> list[str]:
    if isinstance(type_field, list):
        return list(type_field)
    return [type_field]


def cpa_file_url(repo_root: Path, relative_subdir: str) -> str:
    """CPA CLI expects file://<repo>?subdir=<path> (not a bare dir URL)."""
    return f"file://{repo_root.resolve()}?subdir={relative_subdir}"


def template_file_url(repo_root: Path, template: dict[str, Any]) -> str:
    directory = template_dir(template)
    if not directory:
        raise ValueError(f"Cannot resolve directory for template slug={template.get('slug')}")
    return cpa_file_url(repo_root, f"templates/{directory}")


def extension_file_url(repo_root: Path, extension: dict[str, Any]) -> str:
    directory = extension_dir(extension)
    if not directory:
        raise ValueError(f"Cannot resolve directory for extension slug={extension.get('slug')}")
    return cpa_file_url(repo_root, f"extensions/{directory}")


def canonical_template_dir_for_type(type_name: str) -> str | None:
    return CANONICAL_TEMPLATE_BY_TYPE.get(type_name)


def find_template_by_dir(registry: dict[str, Any], directory: str) -> dict[str, Any] | None:
    for template in registry.get("templates", []):
        if template_dir(template) == directory:
            return template
    return None


def has_incompatibility(selected: list[dict[str, Any]], candidate: dict[str, Any]) -> bool:
    candidate_slugs = {candidate["slug"]}
    selected_slugs = {ext["slug"] for ext in selected}
    for ext in selected:
        incompatible = ext.get("incompatibleWith") or []
        if any(slug in candidate_slugs for slug in incompatible):
            return True
        candidate_incompatible = candidate.get("incompatibleWith") or []
        if any(slug in selected_slugs for slug in candidate_incompatible):
            return True
    return False


def load_profiles() -> list[dict[str, Any]]:
    if not PROFILES_DIR.is_dir():
        return []
    profiles: list[dict[str, Any]] = []
    for path in sorted(PROFILES_DIR.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        profiles.append({**profile, "_file": path.name})
    return profiles


def resolve_profile_addons(
    registry: dict[str, Any], profile: dict[str, Any]
) -> list[dict[str, Any]]:
    addons: list[dict[str, Any]] = []
    for slug in profile.get("addons") or []:
        ext = next((e for e in registry.get("extensions", []) if e["slug"] == slug), None)
        if not ext:
            raise ValueError(f'Profile {profile.get("id")}: unknown addon slug "{slug}"')
        addons.append(ext)
    return addons


def assert_profile_valid(
    registry: dict[str, Any], profile: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    template = find_template_by_dir(registry, profile["templateDir"])
    if not template:
        raise ValueError(
            f'Profile {profile.get("id")}: unknown templateDir "{profile.get("templateDir")}"'
        )
    addons = resolve_profile_addons(registry, profile)
    categories: dict[str, str] = {}
    for ext in addons:
        category = ext.get("category")
        if category in categories:
            raise ValueError(
                f'Profile {profile.get("id")}: category "{category}" used twice '
                f'({categories[category]} and {ext["slug"]})'
            )
        categories[category] = ext["slug"]

        template_types = as_types(template.get("type"))
        ext_types = as_types(ext.get("type"))
        if not any(t in ext_types for t in template_types):
            raise ValueError(
                f'Profile {profile.get("id")}: addon "{ext["slug"]}" does not support '
                f'template type(s) {template_types}'
            )

    selected: list[dict[str, Any]] = []
    for ext in addons:
        if has_incompatibility(selected, ext):
            raise ValueError(
                f'Profile {profile.get("id")}: incompatible addons involving {ext["slug"]}'
            )
        selected.append(ext)
    return template, addons


def on_disk_path_for_entry(kind: str, entry: dict[str, Any]) -> Path | None:
    directory = template_dir(entry) if kind == "template" else extension_dir(entry)
    if not directory:
        return None
    return REPO_ROOT / ("templates" if kind == "template" else "extensions") / directory
