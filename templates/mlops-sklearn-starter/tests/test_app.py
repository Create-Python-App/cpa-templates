"""FastAPI serving endpoint tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from mlflow import MlflowClient

from mlops_sklearn.pipeline.run import run_pipeline
from mlops_sklearn.serving.app import app


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")
    result = run_pipeline(Path("configs/default.yaml"))
    experiment_name = result["config"].experiment_name
    version = result["model_version"]
    MlflowClient().set_registered_model_alias(experiment_name, "production", version)
    monkeypatch.setenv("MODEL_URI", f"models:/{experiment_name}@production")
    return TestClient(app)


def test_predict_endpoint_roundtrip(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={"features": [[0.1] * 8, [0.2] * 8]},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["predictions"]) == 2
    assert set(body["predictions"]) <= {0, 1}


def test_predict_endpoint_missing_model_returns_404(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # model_uri is server-configured, not caller-supplied (see app.py) — to
    # exercise the missing-model path, reconfigure the server's MODEL_URI
    # env var, not the request body.
    monkeypatch.setenv("MODEL_URI", "models:/does-not-exist@production")
    response = client.post(
        "/predict",
        json={"features": [[0.1] * 8]},
    )
    assert response.status_code == 404
