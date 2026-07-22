"""Typed experiment config loaded from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    type: str = "logistic_regression"
    max_iter: int = 200


class DataConfig(BaseModel):
    n_samples: int = 200
    n_features: int = 8
    test_size: float = 0.25


class ExperimentConfig(BaseModel):
    experiment_name: str = "mlops-sklearn-local"
    random_seed: int = 42
    model: ModelConfig = Field(default_factory=ModelConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    steps: list[str] = Field(
        default_factory=lambda: ["load_synthetic", "train_classifier", "evaluate"]
    )


def load_config(path: Path | str) -> ExperimentConfig:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ExperimentConfig.model_validate(raw)
