# Contributing

## Quick Start

1. Fork the repository and create a branch from `main`.
2. Add or modify a pipeline step under `data/` or `models/`, implementing
   `BaseStep` from `pipeline/base.py`.
3. Register it in `pipeline/steps_registry.py`.
4. Add or update its config section in `config.py` and `configs/default.yaml`.
5. Add tests — see `docs/TESTING_GUIDE.md`.
6. Run `uv run ruff check .`, `uv run mypy .`, `uv run pyright`, and
   `uv run pytest` before committing.

See `docs/MLOPS_PIPELINE.md` for the full pipeline contract.

## First PR Checklist

This checklist is for contributors making their first pull request to an
MLOps template. Every item must pass before requesting review.

### Project topology & quality bar

- [ ] New pipeline steps are organized under `data/` or `models/` (not a
  single training script at the repo root).
- [ ] Each step implements `BaseStep` from `pipeline/base.py`.
- [ ] New steps are registered in `pipeline/steps_registry.py`.
- [ ] Config sections are added to both `config.py` and `configs/default.yaml`
  with matching defaults.
- [ ] `uv run ruff check .` passes with no errors.
- [ ] `uv run mypy .` and/or `uv run pyright` pass with no errors.
- [ ] Code follows the existing style (4-space indent, type hints, docstrings).

### Testing

- [ ] Tests are **CPU-only** — no GPU/CUDA dependencies required.
- [ ] Tests use small synthetic or bundled fixture data, not external datasets.
- [ ] No network calls in tests (no HTTP requests, no remote API calls).
- [ ] No mandatory remote MLflow server — tests run against a local or
  in-memory tracking store.
- [ ] Secrets are placeholders only (e.g., `YOUR_API_KEY`, never committed values).
- [ ] `uv run pytest` passes in under 5 minutes on a CI runner.
- [ ] Tests cover both happy-path and edge cases for new functionality.

### Template registration

- [ ] New templates are registered in `templates.json` with all required fields:
  `name`, `slug`, `description`, `url`, `type`, `category`, `labels`.
- [ ] New templates have a `docs/README.md.append` describing the template's
  purpose and unique features.
- [ ] New templates have a `.python-version` and `.editorconfig` file.

### CI & infrastructure

- [ ] No GitHub Actions are embedded in the base template — CI/CT/CD is
  delivered via the `all-mlops-github-actions` extension.
- [ ] No `L2` or `L3` CI profiles that depend on external services.
- [ ] `L1` bare CI job passes (syntax check, lint, unit tests only).

### Before submitting

- [ ] Branch is based on the latest `main` (rebase if needed).
- [ ] Commit messages follow conventional commits (`feat:`, `fix:`, `docs:`, etc.).
- [ ] PR title clearly describes the change.
- [ ] PR description references the related issue (if any) and explains:
  - What changed and why.
  - How it was tested.
  - Any trade-offs or limitations.
