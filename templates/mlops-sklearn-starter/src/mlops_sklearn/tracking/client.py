"""MLflow tracking client wrappers — experiment tracking only, not app logging."""

from __future__ import annotations

import os
from typing import Any

import mlflow
from mlflow.data.dataset import Dataset


def configure_tracking(experiment_name: str) -> None:
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def log_params(params: dict[str, Any]) -> None:
    mlflow.log_params(params)


def log_dataset(dataset: Dataset, context: str) -> None:
    mlflow.log_input(dataset, context=context)
