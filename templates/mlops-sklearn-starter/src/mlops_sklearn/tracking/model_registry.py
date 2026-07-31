"""MLflow Model Registry helpers — alias-based, never the deprecated stage API."""

from __future__ import annotations

from typing import Any, cast

import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline


def register_model_version(model: Any, name: str, run_id: str) -> str:
    """Log the fitted pipeline under the active run and register a new version.

    Returns the new model version number as a string. Never sets the
    "production" alias — promotion is a deliberate, separate gate (the
    future model-quality-gate CI job), never automatic here.
    """
    mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=name)
    client = MlflowClient()
    # Scope the lookup to this run specifically — searching by name alone
    # would return the highest version across ALL runs ever registered
    # under this name, which could pick up a different run's version under
    # concurrent training jobs.
    versions = client.search_model_versions(f"name='{name}' and run_id='{run_id}'")
    latest = max(versions, key=lambda v: int(v.version))
    return latest.version


def load_model(model_uri: str) -> Pipeline:
    return cast(Pipeline, mlflow.sklearn.load_model(model_uri))
