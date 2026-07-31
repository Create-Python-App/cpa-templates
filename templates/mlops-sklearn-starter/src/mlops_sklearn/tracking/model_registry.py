"""MLflow Model Registry helpers — alias-based, never the deprecated stage API."""

from __future__ import annotations

from typing import Any, cast

import mlflow.sklearn
from sklearn.pipeline import Pipeline


def register_model_version(model: Any, name: str, run_id: str) -> str:
    """Log the fitted pipeline under the active run and register a new version.

    Returns the new model version number as a string. Never sets the
    "production" alias — promotion is a deliberate, separate gate (the
    future model-quality-gate CI job), never automatic here.

    `run_id` is not used for a lookup (see below) but is kept in the
    signature to document which run's fit this version corresponds to, and
    for drop-in compatibility with callers (`models/train.py` passes
    `run.info.run_id`).

    Implementation note: this used to look up the new version via
    `MlflowClient.search_model_versions(f"name='{name}' and run_id='{run_id}'")`,
    which broke on an apostrophe in `name` (unescaped filter-string
    interpolation) and on `max()` over an empty result. `mlflow.sklearn.log_model`'s
    returned `ModelInfo.registered_model_version` (verified populated and
    correctly incrementing against installed mlflow 3.15.0) gives the new
    version directly, eliminating both the injection risk and the
    empty-result crash.
    """
    info = mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=name)
    version = info.registered_model_version
    if version is None:
        raise RuntimeError(f"model registration for {name!r} did not return a version")
    return str(version)


def load_model(model_uri: str) -> Pipeline:
    return cast(Pipeline, mlflow.sklearn.load_model(model_uri))
