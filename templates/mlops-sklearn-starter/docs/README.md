# mlops-sklearn-starter

CPU-first MLOps pipeline for tabular classification with scikit-learn,
MLflow tracking, and a typed step pipeline. See
[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for the full layout and
[MLOPS_PIPELINE.md](./MLOPS_PIPELINE.md) for how the pipeline and step
registry work.

## Quickstart

```sh
uv sync
uv run mlops-train
uv run pytest
```
