# mlops-sklearn-starter

CPU-first MLOps pipeline for tabular classification with scikit-learn,
MLflow tracking, and a typed step pipeline.

## Quickstart

```sh
uv sync
uv run mlops-train
uv run pytest
```

## Resources

- [Project Structure](./PROJECT_STRUCTURE.md) — the layout above, folder-by-folder
- [MLOps Pipeline](./MLOPS_PIPELINE.md) — the `BaseStep` contract, `STEP_REGISTRY`, and how to add a step
- [Configuration](./CONFIGURATION.md) — `configs/default.yaml` fields and `.env.example` vars
- [Testing Guide](./TESTING_GUIDE.md) — the test categories and how to run them
- [Deployment](./DEPLOYMENT.md) — which serving mode this template uses and why
- [Typing](./TYPING.md) — pydantic v2 + mypy/pyright conventions
