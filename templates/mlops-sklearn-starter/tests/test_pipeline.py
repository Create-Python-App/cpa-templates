"""Data stage step tests."""

from __future__ import annotations

from pathlib import Path

from sklearn.preprocessing import StandardScaler

from mlops_sklearn.config import load_config
from mlops_sklearn.data.features import FeaturesStep
from mlops_sklearn.data.loading import LoadingStep
from mlops_sklearn.data.preprocessing import PreprocessingStep


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
    # Unfitted: StandardScaler has no mean_ attribute until .fit() is called.
    assert not hasattr(context["preprocessor"], "mean_")


def test_features_step_defaults_to_passthrough() -> None:
    context = FeaturesStep().run(_base_context())
    assert context["feature_transformer"] == "passthrough"
