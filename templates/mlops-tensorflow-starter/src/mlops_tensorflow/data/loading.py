"""Generate a tiny synthetic classification dataset (offline) and split it.

Split happens here, not as a separate step, to avoid data leakage: any
later preprocessing/statistic fitting must only ever see the train split.

Pure NumPy + tf.data — no scikit-learn dependency in this template.
"""

from __future__ import annotations

import numpy as np
import tensorflow as tf

from mlops_tensorflow.config import ExperimentConfig
from mlops_tensorflow.pipeline.base import BaseStep, StepContext


def _make_blobs(
    n_samples: int, n_features: int, seed: int
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    half = n_samples // 2
    first = rng.normal(loc=2.0, scale=1.0, size=(half, n_features))
    second = rng.normal(loc=-2.0, scale=1.0, size=(n_samples - half, n_features))
    x = np.vstack([first, second]).astype(np.float32)
    y = np.concatenate(
        [np.zeros(half, dtype=np.int64), np.ones(n_samples - half, dtype=np.int64)]
    )
    perm = rng.permutation(n_samples)
    return x[perm], y[perm]


class LoadingStep(BaseStep):
    name = "loading"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x, y = _make_blobs(cfg.loading.n_samples, cfg.loading.n_features, cfg.random_seed)
        n_train = round(cfg.loading.n_samples * (1 - cfg.loading.test_size))
        x_train, x_test = x[:n_train], x[n_train:]
        y_train, y_test = y[:n_train], y[n_train:]

        # Pre-shuffled above; no dataset-level shuffle keeps the fit loop
        # fully deterministic under the configured seed.
        train_loader = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(
            cfg.training.batch_size
        )
        test_loader = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(1024)
        context.update(
            {
                "x_train": x_train,
                "x_test": x_test,
                "y_train": y_train,
                "y_test": y_test,
                "train_loader": train_loader,
                "test_loader": test_loader,
                "n_features": cfg.loading.n_features,
            }
        )
        return context
