"""Config-driven distribution strategies for TensorFlow starters.

``single`` (default) pins execution to CPU:0 and always works.
``mirrored`` uses ``tf.distribute.MirroredStrategy`` — on a single CPU that
is one replica, so CI stays green while the code path is real. Multi-GPU /
multi-worker strategies are a documented graduation, not a default.
"""

from __future__ import annotations

import tensorflow as tf

_STRATEGIES = ("single", "mirrored")


def get_strategy(kind: str = "single") -> tf.distribute.Strategy:
    """Return the distribution strategy for ``kind`` (config-driven)."""
    if kind not in _STRATEGIES:
        raise ValueError(f"unknown strategy {kind!r}; supported: {_STRATEGIES}")
    if kind == "mirrored":
        return tf.distribute.MirroredStrategy()
    return tf.distribute.OneDeviceStrategy("/cpu:0")


def num_replicas(kind: str = "single") -> int:
    """Replica count for ``kind`` — 1 on CI hardware by construction."""
    return int(get_strategy(kind).num_replicas_in_sync)
