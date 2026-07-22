# Agent notes — mlops-sklearn-starter

- Package lives under `mlops_sklearn/`.
- Training and serving entrypoints are console scripts in `pyproject.toml`.
- Tests must stay offline (no remote MLflow, no dataset downloads).
- Do not add GitHub Actions here — use the `all-mlops-github-actions` extension.
