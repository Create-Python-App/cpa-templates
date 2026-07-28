"""Data and training stage step tests."""

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


def test_training_smoke_without_evaluate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Exercises run_pipeline() through training, before evaluate exists (Task 4).

    Uses a temporary config with a truncated steps list, since the real
    default config's steps: list includes "evaluate", which isn't
    registered until Task 4.
    """
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")

    config_path = tmp_path / "no_evaluate.yaml"
    config_path.write_text(
        "experiment_name: mlops-sklearn-test\n"
        "random_seed: 42\n"
        "steps: [loading, preprocessing, features, model, training]\n"
        "loading:\n  n_samples: 200\n  n_features: 8\n  test_size: 0.25\n"
        "preprocessing:\n  scale: true\n"
        "features:\n  polynomial_degree: 1\n"
        "model:\n  type: logistic_regression\n  max_iter: 200\n"
        "training:\n  cv_folds: 1\n"
        'serving:\n  model_uri: "models:/mlops-sklearn-test@production"\n',
        encoding="utf-8",
    )

    result = run_pipeline(config_path)

    assert "model_version" in result
    # Confirms the scaler-bundling fix: the pipeline was actually fit
    # (fitted attributes present), not just assembled unfitted.
    fitted_scaler = result["model"].named_steps["scaler"]
    assert hasattr(fitted_scaler, "mean_")
