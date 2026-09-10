# Project structure

```text
src/mlops_pytorch/
├── config.py          # ExperimentConfig — one BaseModel per pipeline stage
├── pipeline/           # orchestration only — no ML logic
│   ├── base.py           # BaseStep, StepContext
│   ├── steps_registry.py  # STEP_REGISTRY
│   └── run.py              # run_pipeline(), CLI entrypoint (mlops-train)
├── data/                # Data Processing stage
│   ├── loading.py          # synthetic data + train/test split
│   ├── preprocessing.py     # train-split normalization statistics
│   └── features.py           # passthrough (tabular MLP baseline)
├── models/              # Training & Evaluation stage
│   ├── build.py            # builds the untrained tabular MLP
│   ├── train.py              # fits + registers a new MLflow model version
│   ├── evaluate.py            # metrics + plots + reports/metrics.json
│   └── metrics.py               # compute_metrics()
├── visualization/plots.py  # confusion matrix
├── tracking/             # MLflow-specific concerns only
│   ├── client.py           # tracking URI/experiment/run/dataset wrappers
│   └── model_registry.py    # register/load-by-alias helpers
└── serving/              # Deploying stage
    ├── predict.py           # batch CLI (mlops-predict)
    └── app.py                 # FastAPI POST /predict
```

`configs/default.yaml` — the one experiment config, sections match modules
1:1. `reports/` — gitignored evaluation output. `tests/` — see
[TESTING_GUIDE.md](./TESTING_GUIDE.md).
