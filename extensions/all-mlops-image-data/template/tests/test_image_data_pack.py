"""Tests for the image data pack (schema, shape, determinism, leakage rules)."""

from __future__ import annotations

import numpy as np
import pytest

from data_packs.image import make_images, normalize_images, validate_images


def test_make_images_shape_dtype_and_classes() -> None:
    x, y = make_images(n=16, height=8, width=8, channels=1, seed=4)
    assert x.shape == (16, 8, 8, 1)
    assert x.dtype == np.uint8
    assert set(np.unique(y).tolist()) == {0, 1}


def test_make_images_deterministic_for_same_seed() -> None:
    x1, y1 = make_images(seed=6)
    x2, y2 = make_images(seed=6)
    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)


def test_normalize_images_scales_to_unit_range() -> None:
    x, _ = make_images(n=8, seed=1)
    scaled = normalize_images(x)
    assert scaled.dtype == np.float32
    assert scaled.min() >= 0.0
    assert scaled.max() <= 1.0
    # Idempotent on already-normalized floats.
    assert np.allclose(normalize_images(scaled), scaled)


def test_validate_images_rejects_bad_inputs() -> None:
    x, y = make_images(n=8, seed=2)
    validate_images(x, y)
    validate_images(normalize_images(x), y)
    with pytest.raises(ValueError, match="NHWC"):
        validate_images(x[0], y[:1])
    with pytest.raises(ValueError, match="\\[0, 1\\]"):
        validate_images(x.astype(np.float32) * 2.0, y)
    with pytest.raises(ValueError, match="count mismatch"):
        validate_images(x, y[:4])
    with pytest.raises(ValueError, match="two classes"):
        validate_images(x, np.zeros(8, dtype=np.int64))
