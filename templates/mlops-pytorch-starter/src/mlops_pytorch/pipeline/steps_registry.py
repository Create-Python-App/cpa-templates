"""Step registry mapping config step names to BaseStep implementations."""

from __future__ import annotations

from mlops_pytorch.data.features import FeaturesStep
from mlops_pytorch.data.loading import LoadingStep
from mlops_pytorch.data.preprocessing import PreprocessingStep
from mlops_pytorch.models.build import BuildModelStep
from mlops_pytorch.models.evaluate import EvaluateStep
from mlops_pytorch.models.train import TrainStep
from mlops_pytorch.pipeline.base import BaseStep

STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "loading": LoadingStep,
    "preprocessing": PreprocessingStep,
    "features": FeaturesStep,
    "model": BuildModelStep,
    "training": TrainStep,
    "evaluate": EvaluateStep,
}
