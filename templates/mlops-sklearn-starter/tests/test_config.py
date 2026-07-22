from pathlib import Path

from mlops_sklearn.config import load_config


def test_load_default_config() -> None:
    cfg = load_config(Path("configs/default.yaml"))
    assert cfg.model.type == "logistic_regression"
    assert "train_classifier" in cfg.steps
