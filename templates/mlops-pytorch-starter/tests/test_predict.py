"""Batch serving tests — trains a model inline via fixture, then predicts."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from mlflow import MlflowClient

from mlops_pytorch.pipeline.run import run_pipeline
from mlops_pytorch.serving.predict import predict


@pytest.fixture()
def trained_model_uri(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")
    result = run_pipeline(Path("configs/default.yaml"))
    experiment_name = result["config"].experiment_name
    version = result["model_version"]

    # Promotion is never automatic in the pipeline itself (the future
    # model-quality-gate CI job's job) — simulate it here so serving tests
    # have a "production" alias to load.
    MlflowClient().set_registered_model_alias(experiment_name, "production", version)
    return f"models:/{experiment_name}@production"


def test_predict_on_raw_unscaled_input(trained_model_uri: str) -> None:
    # Raw, unscaled features — proves the bundled normalization inside the
    # registered NormalizedMLP transforms them correctly on its own; nothing
    # here separately loads or applies normalization.
    raw_features = np.random.RandomState(0).normal(size=(3, 8))
    predictions = predict(trained_model_uri, raw_features)
    assert predictions.shape == (3,)
    assert set(predictions.tolist()) <= {0, 1}
