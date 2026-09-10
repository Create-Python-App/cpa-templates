"""Step registry mapping config step names to BaseStep implementations."""

from __future__ import annotations

from mlops_tensorflow.data.features import FeaturesStep
from mlops_tensorflow.data.loading import LoadingStep
from mlops_tensorflow.data.preprocessing import PreprocessingStep
from mlops_tensorflow.models.build import BuildModelStep
from mlops_tensorflow.models.evaluate import EvaluateStep
from mlops_tensorflow.models.train import TrainStep
from mlops_tensorflow.pipeline.base import BaseStep

STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "loading": LoadingStep,
    "preprocessing": PreprocessingStep,
    "features": FeaturesStep,
    "model": BuildModelStep,
    "training": TrainStep,
    "evaluate": EvaluateStep,
}
