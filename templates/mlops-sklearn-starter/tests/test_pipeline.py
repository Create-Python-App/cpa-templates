"""Data, training, and evaluation stage step tests, plus the full pipeline smoke test."""

from __future__ import annotations

from pathlib import Path

import pytest
from sklearn.preprocessing import StandardScaler

from mlops_sklearn.config import load_config
from mlops_sklearn.data.features import FeaturesStep
from mlops_sklearn.data.loading import LoadingStep
from mlops_sklearn.data.preprocessing import PreprocessingStep
from mlops_sklearn.pipeline.run import run_pipeline


def _base_context() -> dict:
    cfg = load_config(Path("configs/default.yaml"))
    return {"config": cfg}


def test_loading_step_produces_expected_shapes() -> None:
    context = LoadingStep().run(_base_context())
    cfg = context["config"]
    expected_train = round(cfg.loading.n_samples * (1 - cfg.loading.test_size))
    assert context["x_train"].shape[0] == expected_train
    assert context["x_train"].shape[1] == cfg.loading.n_features
    assert context["x_test"].shape[0] == cfg.loading.n_samples - expected_train
    assert context["dataset"] is not None


def test_preprocessing_step_stashes_unfitted_scaler() -> None:
    context = PreprocessingStep().run(_base_context())
    assert isinstance(context["preprocessor"], StandardScaler)
    assert not hasattr(context["preprocessor"], "mean_")


def test_features_step_defaults_to_passthrough() -> None:
    context = FeaturesStep().run(_base_context())
    assert context["feature_transformer"] == "passthrough"


def test_full_pipeline_smoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")

    result = run_pipeline(Path("configs/default.yaml"))

    assert "metrics" in result
    assert result["metrics"]["accuracy"] >= 0.0
    assert "model_version" in result
    fitted_scaler = result["model"].named_steps["scaler"]
    assert hasattr(fitted_scaler, "mean_")
    assert Path("reports/metrics.json").exists()
