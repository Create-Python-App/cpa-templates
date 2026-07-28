"""MLflow tracing helpers (fastapi-mlflow-tracing extension).

Security: this module never logs authentication headers, authorization tokens,
API keys, passwords, or raw request bodies. Only HTTP method, URL path, and
status code are recorded as span attributes by the middleware.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class MLflowTracingSettings(BaseSettings):
    """Pydantic-settings backed configuration for MLflow tracing.

    All fields map to environment variables of the same name (case-insensitive).
    Tracing is **disabled by default** — set ``MLFLOW_ENABLED=true`` to opt in.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    mlflow_enabled: bool = False
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "fastapi-app"


# We instantiate settings once globally, just like telemetry.py reads env vars.
# We also provide a way to inject settings for testing.
_global_settings: MLflowTracingSettings | None = None


def _get_settings() -> MLflowTracingSettings:
    global _global_settings
    if _global_settings is None:
        _global_settings = MLflowTracingSettings()
    return _global_settings


def configure_mlflow_tracing() -> None:
    """Enable MLflow tracing when MLFLOW_ENABLED is truthy.

    Sets the tracking URI and active experiment.
    
    No-op when MLFLOW_ENABLED is false.
    """
    settings = _get_settings()
    if not settings.mlflow_enabled:
        return

    import mlflow

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)


@contextmanager
def maybe_start_span(
    name: str,
    **attributes: str | float | bool,
) -> Generator[Any, None, None]:
    """Context manager that wraps a block of code in an MLflow span.

    No-op (yields immediately) when tracing is disabled. Never record
    secret values in ``attributes``.

    Example::

        with maybe_start_span("my-operation", custom_key="value") as span:
            do_work()
    """
    settings = _get_settings()
    if not settings.mlflow_enabled:
        yield None
        return

    import mlflow

    with mlflow.start_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, value)
        yield span


def set_attribute(key: str, value: str | float | bool) -> None:
    """Set an attribute on the currently active MLflow span.
    
    No-op when tracing is disabled.
    """
    settings = _get_settings()
    if not settings.mlflow_enabled:
        return

    import mlflow
    
    active_span = mlflow.get_current_active_span()
    if active_span:
        active_span.set_attribute(key, value)
