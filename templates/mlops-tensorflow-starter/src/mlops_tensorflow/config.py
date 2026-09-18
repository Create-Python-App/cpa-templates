"""Typed experiment config loaded from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class LoadingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    n_samples: int = 200
    n_features: int = 8
    test_size: float = 0.25


class PreprocessingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scale: bool = True


class FeaturesConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    polynomial_degree: int = 1


class ModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = "mlp_classifier"
    hidden_dim: int = 16


class TrainingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    epochs: int = 5
    lr: float = 0.01
    batch_size: int = 32


class ServingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_uri: str = "models:/mlops-tensorflow-local@production"


class ExperimentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    experiment_name: str = "mlops-tensorflow-local"
    random_seed: int = 42
    steps: list[str] = Field(
        default_factory=lambda: [
            "loading",
            "preprocessing",
            "features",
            "model",
            "training",
            "evaluate",
        ]
    )
    loading: LoadingConfig = Field(default_factory=LoadingConfig)
    preprocessing: PreprocessingConfig = Field(default_factory=PreprocessingConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    serving: ServingConfig = Field(default_factory=ServingConfig)


def load_config(path: Path | str) -> ExperimentConfig:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ExperimentConfig.model_validate(raw)
