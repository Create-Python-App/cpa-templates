"""Framework-agnostic image data helpers — synthetic images, normalization,
and validation. NumPy only (uint8 NHWC convention): no Pillow/torch/TF
dependency, so every MLOps starter can use this pack unchanged.
"""

from __future__ import annotations

import numpy as np


def make_images(
    n: int = 32,
    height: int = 16,
    width: int = 16,
    channels: int = 1,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Two-pattern synthetic images (bright square vs. dark square) as uint8
    NHWC plus binary labels, shuffled deterministically."""
    rng = np.random.default_rng(seed)
    images = np.zeros((n, height, width, channels), dtype=np.uint8)
    labels = np.zeros(n, dtype=np.int64)
    half = n // 2
    h0, w0 = height // 4, width // 4
    h1, w1 = h0 + height // 2, w0 + width // 2
    images[:half, h0:h1, w0:w1, :] = 220
    labels[:half] = 1
    noise = rng.integers(0, 30, size=images.shape).astype(np.uint8)
    images = (images.astype(np.int32) + noise.astype(np.int32)).clip(0, 255).astype(
        np.uint8
    )
    perm = rng.permutation(n)
    return images[perm], labels[perm]


def normalize_images(x: np.ndarray) -> np.ndarray:
    """Scale uint8 ``[0, 255]`` to float32 ``[0, 1]`` (idempotent on floats)."""
    arr = np.asarray(x)
    if arr.dtype == np.uint8:
        return (arr.astype(np.float32) / 255.0).astype(np.float32)
    result: np.ndarray = np.asarray(arr, dtype=np.float32)
    return result


def validate_images(x: np.ndarray, y: np.ndarray | None = None) -> None:
    """Schema/shape rules for image batches; raises ValueError on violation."""
    x = np.asarray(x)
    if x.ndim != 4:
        raise ValueError(f"expected NHWC (n, h, w, c), got shape {x.shape}")
    if 0 in x.shape:
        raise ValueError(f"empty image batch with shape {x.shape}")
    if x.dtype == np.uint8:
        pass
    elif np.issubdtype(x.dtype, np.floating):
        if x.min(initial=0.0) < 0.0 or x.max(initial=1.0) > 1.0:
            raise ValueError("float images must be in [0, 1]")
    else:
        raise ValueError(f"images must be uint8 or float, got {x.dtype}")
    if y is not None:
        y = np.asarray(y)
        if y.shape[0] != x.shape[0]:
            raise ValueError(
                f"count mismatch: {x.shape[0]} images, {y.shape[0]} labels"
            )
        if np.unique(y).size < 2:
            raise ValueError("labels must contain at least two classes")
