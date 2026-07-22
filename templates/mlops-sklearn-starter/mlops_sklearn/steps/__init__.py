"""Pipeline steps."""

from mlops_sklearn.steps.base import BaseStep, StepContext
from mlops_sklearn.steps.evaluate import EvaluateStep
from mlops_sklearn.steps.load_synthetic import LoadSyntheticStep
from mlops_sklearn.steps.train_classifier import TrainClassifierStep

STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "load_synthetic": LoadSyntheticStep,
    "train_classifier": TrainClassifierStep,
    "evaluate": EvaluateStep,
}

__all__ = ["BaseStep", "STEP_REGISTRY", "StepContext"]
