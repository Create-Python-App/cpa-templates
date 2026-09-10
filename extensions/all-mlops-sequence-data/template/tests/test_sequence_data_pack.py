"""Tests for the sequence data pack (schema, shape, determinism, leakage rules)."""

from __future__ import annotations

import numpy as np
import pytest

from data_packs.sequence import (
    make_series,
    sliding_windows,
    temporal_split,
    validate_series,
)


def test_make_series_shape_dtype_and_determinism() -> None:
    a = make_series(n_series=4, length=32, n_features=2, seed=9)
    b = make_series(n_series=4, length=32, n_features=2, seed=9)
    assert a.shape == (4, 32, 2)
    assert a.dtype == np.float32
    assert np.array_equal(a, b)


def test_sliding_windows_counts_and_shapes() -> None:
    series = make_series(n_series=2, length=20, n_features=3, seed=1)
    xs, ys = sliding_windows(series, window=8, horizon=2)
    # 20 - 8 - 2 + 1 = 11 windows per series
    assert xs.shape == (2, 11, 8, 3)
    assert ys.shape == (2, 11)
    # Target equals the first feature `horizon` steps after each window end.
    assert np.allclose(ys[0, 0], series[0, 8 + 2 - 1, 0])


def test_sliding_windows_rejects_short_series() -> None:
    series = make_series(n_series=1, length=10, n_features=2, seed=1)
    with pytest.raises(ValueError, match="too short"):
        sliding_windows(series, window=8, horizon=4)


def test_temporal_split_never_shuffles_time() -> None:
    train_idx, test_idx = temporal_split(100, test_size=0.2)
    assert len(train_idx) == 80
    assert len(test_idx) == 20
    # Leakage rule: the whole train block precedes the test block.
    assert train_idx.max() < test_idx.min()
    assert np.array_equal(train_idx, np.arange(80))
    assert np.array_equal(test_idx, np.arange(80, 100))


def test_validate_series_rejects_bad_inputs() -> None:
    validate_series(make_series(n_series=2, length=16, n_features=2, seed=2))
    with pytest.raises(ValueError, match="n_series"):
        validate_series(np.zeros((16, 2), dtype=np.float32))
    with pytest.raises(ValueError, match="NaN"):
        bad = make_series(n_series=2, length=16, n_features=2, seed=2)
        bad[0, 0, 0] = np.nan
        validate_series(bad)
