"""Framework-agnostic tabular data helpers — synthetic generation, splitting,
standardization, and validation. NumPy only: no sklearn/PyTorch/TensorFlow
dependency, so every MLOps starter can use this pack unchanged.
"""

from __future__ import annotations

import numpy as np


def make_tabular_classification(
    n_samples: int = 200, n_features: int = 8, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """Two Gaussian blobs (binary labels), shuffled deterministically."""
    rng = np.random.default_rng(seed)
    half = n_samples // 2
    first = rng.normal(loc=2.0, scale=1.0, size=(half, n_features))
    second = rng.normal(loc=-2.0, scale=1.0, size=(n_samples - half, n_features))
    x = np.vstack([first, second]).astype(np.float32)
    y = np.concatenate(
        [np.zeros(half, dtype=np.int64), np.ones(n_samples - half, dtype=np.int64)]
    )
    return x[rng.permutation(n_samples)], y[rng.permutation(n_samples)]


def split_indices(
    n: int, test_size: float = 0.25, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """Disjoint shuffled train/test index arrays (no leakage by construction)."""
    if not 0.0 < test_size < 1.0:
        raise ValueError(f"test_size must be in (0, 1), got {test_size}")
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    n_test = round(n * test_size)
    return perm[: n - n_test], perm[n - n_test :]


def fit_standardizer(x_train: np.ndarray) -> dict[str, np.ndarray]:
    """Fit mean/std on the TRAIN split only — never on the holdout."""
    x = np.asarray(x_train, dtype=np.float32)
    if x.ndim != 2:
        raise ValueError(f"expected a 2D feature matrix, got shape {x.shape}")
    return {"mean": x.mean(axis=0), "std": x.std(axis=0)}


def apply_standardizer(
    x: np.ndarray, stats: dict[str, np.ndarray]
) -> np.ndarray:
    """Apply train-split stats to any split (train, holdout, or serving input)."""
    result: np.ndarray = (np.asarray(x, dtype=np.float32) - stats["mean"]) / np.maximum(
        stats["std"], 1e-8
    )
    return result


def validate_tabular(x: np.ndarray, y: np.ndarray | None = None) -> None:
    """Schema/shape rules for tabular inputs; raises ValueError on violation."""
    x = np.asarray(x)
    if x.ndim != 2:
        raise ValueError(f"expected a 2D feature matrix, got shape {x.shape}")
    if x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError(f"empty feature matrix with shape {x.shape}")
    if not np.isfinite(x).all():
        raise ValueError("feature matrix contains NaN or infinite values")
    if y is not None:
        y = np.asarray(y)
        if y.shape[0] != x.shape[0]:
            raise ValueError(
                f"row mismatch: X has {x.shape[0]} rows, y has {y.shape[0]}"
            )
        if np.unique(y).size < 2:
            raise ValueError("labels must contain at least two classes")
