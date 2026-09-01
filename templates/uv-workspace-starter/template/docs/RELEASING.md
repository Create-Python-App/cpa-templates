# Releasing

Each workspace member is versioned and published independently. There is no
root package to release — the root is virtual.

## Versioning

Bump the `version` in the member's `pyproject.toml` following
[semantic versioning](https://semver.org/). When a library's public API changes,
also bump the members that depend on it if their behavior changes.

## Build

```bash
uv build --package app-core        # build a single member
uv build --all-packages            # build every member
```

Artifacts land in each member's `dist/` directory.

## Publish

```bash
# Configure credentials once (token via env var or `~/.pypirc`).
uv publish --package app-core
```

For private indexes, pass `--publish-url` (or set `UV_PUBLISH_URL`).

## Suggested flow

1. Update the member's `version` and its `CHANGELOG` (if you keep one).
2. `make check` — lint, type-check, and test the whole workspace.
3. `uv build --package <name>`.
4. `uv publish --package <name>`.
5. Tag the release, e.g. `git tag <name>-vX.Y.Z && git push --tags`.

> Prefer automation? Wire these steps into a GitHub Actions workflow — the
> `github-setup` extension provides a starting CI pipeline.
