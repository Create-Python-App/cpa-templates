# Template quality checklist (M1)

Use this checklist before calling the sklearn MLOps starter "mature" for CPA.

## Required

- [x] README documents run / train / test (`uv sync`, `uv run mlops-train`, `uv run pytest`)
- [x] Serving modes exist: batch `mlops-predict` CLI + FastAPI `POST /predict`, both loading the registered model by URI (never retraining)
- [x] Serving covered by pytest (`test_predict.py` / `test_app.py`, promoting a trained version to the `production` alias in-test)
- [x] `.env.example` documents `MLFLOW_TRACKING_URI` and `MODEL_URI` used by serving and tracking
- [x] `uv sync` + `uv run ruff check .` + `uv run pytest` pass after scaffold (CI L1)
- [x] CPU-first: no CUDA-only dependency is ever required for `uv sync` or tests to pass
- [x] `configs/` directory with environment handling (`configs/default.yaml`, full-file `--config` alternates, `MLFLOW_TRACKING_URI` via env override)
- [x] Data pipeline documented in `docs/MLOPS_PIPELINE.md` (`BaseStep` contract, `STEP_REGISTRY`, registration-vs-promotion split, dataset/preprocessing lineage)
- [x] Docs suite present (`PROJECT_STRUCTURE`, `CONFIGURATION`, `TESTING_GUIDE`, `DEPLOYMENT`, `TYPING`, `MLOPS_PIPELINE`)
- [x] Compatible extensions documented with real catalog slugs (see below)

## Typing (default)

- [x] `mypy` and `pyright` in the dev dependency group
- [x] `[tool.mypy]` (with per-module `ignore_missing_imports` overrides for `sklearn`/`mlflow`) and `[tool.pyright]` configured in `pyproject.toml`
- [x] `docs/TYPING.md` documents `uv run mypy .` and `uv run pyright`

## Promotion gate

Training (`uv run mlops-train`) always registers a new model version but
**never** sets the `production` alias. Serving defaults to
`models:/mlops-sklearn-local@production`. Promote manually once satisfied
with a version's metrics — see [DEPLOYMENT.md](./docs/DEPLOYMENT.md).

## Extension slots (catalog slugs)

| Slug | Role |
|------|------|
| `all-mlops-github-actions` | CI: automated training, quality gates, deployment |
| `all-mlops-tabular-data` | Tabular modality data pack |
| `all-mlops-sequence-data` | Sequence modality data pack |
| `all-mlops-image-data` | Image modality data pack |
| `mlops-sklearn-distributed` | Distributed training for sklearn |
| `github-setup` | GitHub Actions / Dependabot / templates |

Example:

```sh
uvx create-awesome-python-app@latest my-pipeline \
  --template mlops-sklearn-starter \
  --addons all-mlops-github-actions \
  --addons all-mlops-tabular-data \
  --no-interactive
```
