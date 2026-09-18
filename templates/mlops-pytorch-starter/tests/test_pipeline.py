"""Data, training, and evaluation stage step tests, plus the full pipeline smoke test."""

from __future__ import annotations

from pathlib import Path

import pytest
import torch

from mlops_pytorch.config import load_config
from mlops_pytorch.data.features import FeaturesStep
from mlops_pytorch.data.loading import LoadingStep
from mlops_pytorch.data.preprocessing import PreprocessingStep, normalize
from mlops_pytorch.models.build import build_model
from mlops_pytorch.pipeline.run import run_pipeline


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
    assert context["train_loader"] is not None


def test_preprocessing_step_computes_train_stats() -> None:
    context = LoadingStep().run(_base_context())
    context = PreprocessingStep().run(context)
    stats = context["norm_stats"]
    assert stats["mean"].shape[0] == 8
    assert torch.all(stats["std"] > 0)
    normalized = normalize(context["x_train"], stats["mean"], stats["std"])
    assert abs(float(normalized.mean())) < 0.5


def test_features_step_rejects_polynomial_degree() -> None:
    cfg = load_config(Path("configs/default.yaml"))
    cfg.features.polynomial_degree = 2
    with pytest.raises(ValueError, match="polynomial_degree"):
        FeaturesStep().run({"config": cfg})


def test_build_model_rejects_unsupported_model_type() -> None:
    cfg = load_config(Path("configs/default.yaml"))
    cfg.model.type = "resnet"
    with pytest.raises(ValueError, match="unsupported model.type"):
        build_model(cfg, 8)


def test_full_pipeline_smoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")

    result = run_pipeline(Path("configs/default.yaml"))

    assert "metrics" in result
    assert result["metrics"]["accuracy"] >= 0.0
    assert "model_version" in result
    assert Path("model.pt").exists()
    assert Path("model.ts").exists()
    assert Path("reports/metrics.json").exists()
