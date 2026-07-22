from pathlib import Path

from mlops_sklearn.training.train import run_pipeline


def test_train_pipeline_smoke(tmp_path, monkeypatch) -> None:
    db = tmp_path / "mlflow.db"
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{db}")
    result = run_pipeline(Path("configs/default.yaml"))
    assert "model" in result
    assert result["metrics"]["accuracy"] >= 0.0
