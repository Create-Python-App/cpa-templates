"""Offline tests for the MLflow tracing helper.

All tests run without a remote MLflow server. Where MLflow initialization
is exercised, a temporary local ``file://`` tracking directory is used.
Where initialization must be skipped, a mocked mlflow interface is used to
confirm no real calls are made.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI

import app.core.mlflow_tracing
from app.core.mlflow_tracing import (
    MLflowTracingSettings,
    configure_mlflow_tracing,
    maybe_start_span,
    set_attribute,
)


@pytest.fixture(autouse=True)
def reset_global_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset the global settings and env vars before each test to ensure isolation."""
    app.core.mlflow_tracing._global_settings = None
    # mlflow.set_tracking_uri() mutates os.environ in some versions, clean it up
    monkeypatch.delenv("MLFLOW_TRACKING_URI", raising=False)
    monkeypatch.delenv("MLFLOW_EXPERIMENT_NAME", raising=False)
    monkeypatch.delenv("MLFLOW_ENABLED", raising=False)
    # MLflow 2.15+ warns/errors on file:// store without this flag
    monkeypatch.setenv("MLFLOW_ALLOW_FILE_STORE", "true")


# ---------------------------------------------------------------------------
# 1. Tracing disabled — no MLflow initialization at all
# ---------------------------------------------------------------------------

class TestDisabled:
    def test_configure_does_not_call_mlflow(self) -> None:
        """configure_mlflow_tracing() with disabled settings must not import or call mlflow."""
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=False
        )
        test_app = FastAPI()

        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            configure_mlflow_tracing(test_app)
            mock_mlflow.set_tracking_uri.assert_not_called()
            mock_mlflow.set_experiment.assert_not_called()

        # Check no middleware was added
        # (FastAPI adds 2 middlewares by default: ServerErrorMiddleware, ExceptionMiddleware)
        assert len(test_app.user_middleware) == 0

    def test_maybe_start_span_yields_without_import(self) -> None:
        """maybe_start_span() must yield without importing mlflow when disabled."""
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=False
        )
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            with maybe_start_span("test-span") as span:
                assert span is None
            mock_mlflow.start_span.assert_not_called()

    def test_set_attribute_without_import(self) -> None:
        """set_attribute() must return immediately when disabled."""
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=False
        )
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            set_attribute("key", "value")
            mock_mlflow.get_current_active_span.assert_not_called()


# ---------------------------------------------------------------------------
# 2. Tracing enabled — initializes correctly with local file backend
# ---------------------------------------------------------------------------

class TestEnabled:
    def test_configure_calls_set_tracking_uri(self, tmp_path: Path) -> None:
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=True,
            mlflow_tracking_uri=tmp_path.as_uri(),
            mlflow_experiment_name="test-experiment",
        )
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            configure_mlflow_tracing()
            mock_mlflow.set_tracking_uri.assert_called_once_with(tmp_path.as_uri())

    def test_local_file_backend_no_error(self, tmp_path: Path) -> None:
        """Enabled tracing against a real local file:// URI must not raise."""
        import mlflow
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=True,
            mlflow_tracking_uri=tmp_path.as_uri(),
            mlflow_experiment_name="test-experiment",
        )
        configure_mlflow_tracing()
        assert mlflow.get_tracking_uri() == tmp_path.as_uri()

    def test_middleware_added_when_enabled(self, tmp_path: Path) -> None:
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=True,
            mlflow_tracking_uri=tmp_path.as_uri(),
        )
        test_app = FastAPI()
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            configure_mlflow_tracing(test_app)
            assert len(test_app.user_middleware) == 1
            # mypy complains about .cls not having __name__, so we ignore it
            assert "MLflowTracingMiddleware" in test_app.user_middleware[0].cls.__name__  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# 3. Settings — pydantic-settings defaults and field mapping
# ---------------------------------------------------------------------------

class TestSettings:
    def test_disabled_by_default(self) -> None:
        cfg = MLflowTracingSettings()
        assert cfg.mlflow_enabled is False

    def test_default_tracking_uri(self) -> None:
        cfg = MLflowTracingSettings()
        assert cfg.mlflow_tracking_uri == "http://localhost:5000"

    def test_env_override_via_monkeypatch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MLFLOW_ENABLED", "true")
        monkeypatch.setenv("MLFLOW_TRACKING_URI", "file:///tmp/test")
        cfg = MLflowTracingSettings()
        assert cfg.mlflow_enabled is True
        assert cfg.mlflow_tracking_uri == "file:///tmp/test"


# ---------------------------------------------------------------------------
# 4. mlflow helpers
# ---------------------------------------------------------------------------

class TestMlflowHelpers:
    def test_span_calls_start_span_when_enabled(self, tmp_path: Path) -> None:
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=True,
            mlflow_tracking_uri=tmp_path.as_uri(),
        )
        mock_span = MagicMock()
        mock_span.__enter__ = MagicMock(return_value=mock_span)
        mock_span.__exit__ = MagicMock(return_value=False)
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            mock_mlflow.start_span.return_value = mock_span
            with maybe_start_span("my-span", custom_key="val"):
                pass
            mock_mlflow.start_span.assert_called_once_with("my-span")
            mock_span.set_attribute.assert_called_once_with("custom_key", "val")

    def test_set_attribute_calls_active_span(self) -> None:
        app.core.mlflow_tracing._global_settings = MLflowTracingSettings(
            mlflow_enabled=True,
        )
        mock_span = MagicMock()
        with patch.dict("sys.modules", {"mlflow": MagicMock()}):
            mock_mlflow = sys.modules["mlflow"]
            mock_mlflow.get_current_active_span.return_value = mock_span
            
            set_attribute("key", "val")
            
            mock_mlflow.get_current_active_span.assert_called_once()
            mock_span.set_attribute.assert_called_once_with("key", "val")
