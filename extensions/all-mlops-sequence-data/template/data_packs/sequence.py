"""Framework-agnostic sequence data helpers — synthetic series, windowing,
temporal splitting, and validation. NumPy only: no framework dependency, so
every MLOps starter can use this pack unchanged.
"""

from __future__ import annotations

import numpy as np


def make_series(
    n_series: int = 8, length: int = 64, n_features: int = 3, seed: int = 42
) -> np.ndarray:
    """Sine + trend + noise series, shape ``(n_series, length, n_features)``."""
    rng = np.random.default_rng(seed)
    t = np.arange(length, dtype=np.float32)
    out = np.empty((n_series, length, n_features), dtype=np.float32)
    for s in range(n_series):
        for f in range(n_features):
            phase = rng.uniform(0, 2 * np.pi)
            slope = rng.normal(0, 0.02)
            out[s, :, f] = (
                np.sin(2 * np.pi * t / 16 + phase)
                + slope * t
                + rng.normal(0, 0.1, size=length)
            ).astype(np.float32)
    return out


def sliding_windows(
    series: np.ndarray, window: int = 16, horizon: int = 1
) -> tuple[np.ndarray, np.ndarray]:
    """Cut each ``(length, n_features)`` series into ``(window, n_features)``
    inputs with the value ``horizon`` steps ahead (first feature) as target.
    """
    series = np.asarray(series, dtype=np.float32)
    if series.ndim != 3:
        raise ValueError(f"expected (n_series, length, n_features), got {series.shape}")
    n_windows = series.shape[1] - window - horizon + 1
    if n_windows <= 0:
        raise ValueError(
            f"length {series.shape[1]} too short for window={window}, horizon={horizon}"
        )
    xs = np.stack(
        [series[:, start : start + window, :] for start in range(n_windows)], axis=1
    )
    ys = series[:, window + horizon - 1 : window + horizon - 1 + n_windows, 0]
    return xs, ys


def temporal_split(
    n_steps: int, test_size: float = 0.25
) -> tuple[np.ndarray, np.ndarray]:
    """Contiguous past/future index split — never shuffle time series.

    Leakage rule: every train index precedes every test index.
    """
    if not 0.0 < test_size < 1.0:
        raise ValueError(f"test_size must be in (0, 1), got {test_size}")
    n_test = round(n_steps * test_size)
    train_idx = np.arange(n_steps - n_test)
    test_idx = np.arange(n_steps - n_test, n_steps)
    assert train_idx.max() < test_idx.min()
    return train_idx, test_idx


def validate_series(x: np.ndarray) -> None:
    """Schema/shape rules for series batches; raises ValueError on violation."""
    x = np.asarray(x)
    if x.ndim != 3:
        raise ValueError(f"expected (n_series, length, n_features), got {x.shape}")
    if 0 in x.shape:
        raise ValueError(f"empty series batch with shape {x.shape}")
    if not np.isfinite(x).all():
        raise ValueError("series contains NaN or infinite values")
