# AGENTS.md

This is an `mlops-sklearn-starter`-generated project: a CPU-first sklearn
MLOps pipeline (see `docs/PROJECT_STRUCTURE.md`).

## Key concepts

- `src/mlops_sklearn/pipeline/` is orchestration only — never put ML logic
  there. Domain logic lives in `data/`, `models/`, `tracking/`, `serving/`.
- `configs/default.yaml` sections map 1:1 to code modules — see
  `docs/CONFIGURATION.md`.
- Training always registers a new MLflow model version; it never promotes
  to `production` — see `docs/MLOPS_PIPELINE.md`.

## How to test

```sh
uv sync
uv run ruff check .
uv run mypy .
uv run pytest
```

## Docs

See `docs/README.md` for the full index.
