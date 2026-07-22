# MLOps sklearn starter

CPU-first tabular MLOps project using scikit-learn, YAML configs, step pipelines,
and local MLflow tracking.

## Quick start

```bash
uv sync
uv run mlops-train --config configs/default.yaml
uv run mlops-predict --config configs/default.yaml --input tests/fixtures/sample_predict.csv
uv run pytest
```

## Layout

See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md). Contract:
[docs/MLOPS_CONTRACT.md](https://github.com/Create-Python-App/cpa-templates/blob/main/docs/MLOPS_CONTRACT.md)
(bank-level).
