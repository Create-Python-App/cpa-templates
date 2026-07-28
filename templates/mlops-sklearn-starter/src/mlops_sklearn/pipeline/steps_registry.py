"""Step registry mapping config step names to BaseStep implementations."""

from __future__ import annotations

from mlops_sklearn.data.features import FeaturesStep
from mlops_sklearn.data.loading import LoadingStep
from mlops_sklearn.data.preprocessing import PreprocessingStep
from mlops_sklearn.models.build import BuildModelStep
from mlops_sklearn.models.train import TrainStep
from mlops_sklearn.pipeline.base import BaseStep

STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "loading": LoadingStep,
    "preprocessing": PreprocessingStep,
    "features": FeaturesStep,
    "model": BuildModelStep,
    "training": TrainStep,
}
