# mlops-sklearn-starter

CPU-first sklearn MLOps starter: typed step pipeline, local MLflow tracking,
and batch/FastAPI serving — scaffolded with create-awesome-python-app.

```sh
uv sync
uv run mlops-train
uv run pytest
```

Note: training registers a new model version but does not promote it — see
[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for how to promote a version
before serving.

See [docs/README.md](./docs/README.md) for the full documentation index.
