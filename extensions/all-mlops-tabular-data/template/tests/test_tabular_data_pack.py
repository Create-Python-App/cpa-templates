"""Tests for the tabular data pack (schema, shape, determinism, leakage rules)."""

from __future__ import annotations

import numpy as np
import pytest

from data_packs.tabular import (
    apply_standardizer,
    fit_standardizer,
    make_tabular_classification,
    split_indices,
    validate_tabular,
)


def test_make_tabular_shapes_dtypes_and_classes() -> None:
    x, y = make_tabular_classification(n_samples=100, n_features=4, seed=7)
    assert x.shape == (100, 4)
    assert x.dtype == np.float32
    assert y.shape == (100,)
    assert set(np.unique(y).tolist()) == {0, 1}


def test_make_tabular_deterministic_for_same_seed() -> None:
    x1, y1 = make_tabular_classification(seed=11)
    x2, y2 = make_tabular_classification(seed=11)
    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)


def test_split_indices_are_disjoint_and_cover_all_rows() -> None:
    train_idx, test_idx = split_indices(100, test_size=0.25, seed=3)
    assert len(train_idx) == 75
    assert len(test_idx) == 25
    assert set(train_idx.tolist()).isdisjoint(set(test_idx.tolist()))
    assert set(train_idx.tolist()) | set(test_idx.tolist()) == set(range(100))


def test_split_indices_rejects_bad_test_size() -> None:
    with pytest.raises(ValueError, match="test_size"):
        split_indices(100, test_size=0.0)


def test_standardizer_fits_train_only() -> None:
    # Leakage rule: stats must equal the train-split stats, not full-data stats.
    x, _ = make_tabular_classification(n_samples=100, n_features=4, seed=5)
    train_idx, test_idx = split_indices(100, test_size=0.25, seed=5)
    stats = fit_standardizer(x[train_idx])
    assert np.allclose(stats["mean"], x[train_idx].mean(axis=0))
    assert not np.allclose(stats["mean"], x.mean(axis=0))
    scaled = apply_standardizer(x[test_idx], stats)
    assert scaled.shape == x[test_idx].shape
    assert bool(np.isfinite(scaled).all())


def test_validate_tabular_rejects_bad_inputs() -> None:
    x, y = make_tabular_classification(n_samples=20, n_features=3, seed=1)
    validate_tabular(x, y)
    with pytest.raises(ValueError, match="2D"):
        validate_tabular(x.ravel(), y)
    with pytest.raises(ValueError, match="NaN"):
        bad = x.copy()
        bad[0, 0] = np.nan
        validate_tabular(bad, y)
    with pytest.raises(ValueError, match="row mismatch"):
        validate_tabular(x, y[:10])
    with pytest.raises(ValueError, match="two classes"):
        validate_tabular(x, np.zeros(20, dtype=np.int64))
