"""Config loading tests."""

from pathlib import Path

from mlops_tensorflow.config import load_config


def test_load_default_config() -> None:
    cfg = load_config(Path("configs/default.yaml"))
    assert cfg.model.type == "mlp_classifier"
    assert cfg.loading.n_samples == 200
    assert cfg.serving.model_uri == "models:/mlops-tensorflow-local@production"


def test_default_config_has_full_step_sequence() -> None:
    cfg = load_config(Path("configs/default.yaml"))
    assert cfg.steps == [
        "loading",
        "preprocessing",
        "features",
        "model",
        "training",
        "evaluate",
    ]
