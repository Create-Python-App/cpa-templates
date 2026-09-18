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


def flatten_params(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten a nested config dict into dotted-key params for MLflow logging.

    e.g. {"loading": {"n_samples": 200}} -> {"loading.n_samples": 200}.
    """
    flat: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_params(value, full_key))
        else:
            flat[full_key] = value
    return flat


def log_dataset(dataset: Dataset, context: str) -> None:
    mlflow.log_input(dataset, context=context)
