"""Assemble the (untrained) tabular MLP classifier — CPU-first, tiny by design."""

from __future__ import annotations

from typing import Any, Self, cast

import numpy as np
import tensorflow as tf

from mlops_tensorflow.config import ExperimentConfig
from mlops_tensorflow.pipeline.base import BaseStep, StepContext

_SUPPORTED_MODEL_TYPES = ("mlp_classifier",)


class MLPClassifier(tf.keras.Model):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        # `Model.__new__` is unannotated, so without this the constructor
        # type collapses to `Model[Unknown, Unknown]` for checkers.
        return cast(Self, super().__new__(cls, *args, **kwargs))

    def __init__(self, n_features: int, hidden_dim: int, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._n_features = n_features
        self._hidden_dim = hidden_dim
        self.hidden = tf.keras.layers.Dense(hidden_dim, activation="relu")
        self.logits = tf.keras.layers.Dense(2)

    def call(self, x: tf.Tensor) -> tf.Tensor:
        return self.logits(self.hidden(x))

    def get_config(self) -> dict[str, Any]:
        config: dict[str, Any] = dict(super().get_config())
        config.update({"n_features": self._n_features, "hidden_dim": self._hidden_dim})
        return config


class NormalizedMLP(tf.keras.Model):
    """Serving wrapper: applies train-split normalization, then the MLP.

    Bundling normalization with the weights (like sklearn's Pipeline)
    keeps serving correct without a sidecar stats file.
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        # `Model.__new__` is unannotated, so without this the constructor
        # type collapses to `Model[Unknown, Unknown]` for checkers.
        return cast(Self, super().__new__(cls, *args, **kwargs))

    def __init__(
        self,
        model: MLPClassifier,
        mean: np.ndarray,
        std: np.ndarray,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.model = model
        self.mean = tf.Variable(
            tf.convert_to_tensor(np.asarray(mean, dtype=np.float32)), trainable=False
        )
        self.std = tf.Variable(
            tf.convert_to_tensor(np.maximum(np.asarray(std, dtype=np.float32), 1e-8)),
            trainable=False,
        )

    def call(self, x: tf.Tensor) -> tf.Tensor:
        return self.model((tf.cast(x, tf.float32) - self.mean) / self.std)

    def get_config(self) -> dict[str, Any]:
        config: dict[str, Any] = dict(super().get_config())
        config.update(
            {
                "model": tf.keras.utils.serialize_keras_object(self.model),
                "mean": self.mean.numpy().tolist(),
                "std": self.std.numpy().tolist(),
            }
        )
        return config

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> NormalizedMLP:
        with tf.keras.utils.custom_object_scope({"MLPClassifier": MLPClassifier}):
            model = cast(
                MLPClassifier,
                tf.keras.utils.deserialize_keras_object(config["model"]),
            )
        assert isinstance(model, MLPClassifier)
        return cls(
            model,
            np.asarray(config["mean"], dtype=np.float32),
            np.asarray(config["std"], dtype=np.float32),
        )


def build_model(cfg: ExperimentConfig, n_features: int) -> MLPClassifier:
    if cfg.model.type not in _SUPPORTED_MODEL_TYPES:
        raise ValueError(
            f"unsupported model.type {cfg.model.type!r}; supported: {_SUPPORTED_MODEL_TYPES}"
        )
    tf.keras.utils.set_random_seed(cfg.random_seed)
    return MLPClassifier(n_features=n_features, hidden_dim=cfg.model.hidden_dim)


class BuildModelStep(BaseStep):
    name = "model"

    def validate(self, context: StepContext) -> None:
        if "n_features" not in context:
            raise ValueError("missing n_features in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        context["model"] = build_model(cfg, context["n_features"])
        return context


# Register for ``model.save`` / SavedModel / mlflow round-trips. Done as
# plain calls (not ``@decorators``): the registration helper is untyped, so
# decorating would erase the class types for checkers (every construction
# site would read ``Model[Unknown, Unknown]``).
tf.keras.utils.register_keras_serializable()(MLPClassifier)
tf.keras.utils.register_keras_serializable()(NormalizedMLP)
