"""Tests for distribution strategy selection — CPU fallback behavior."""

from __future__ import annotations

import pytest

from mlops_tensorflow_distributed.strategy import get_strategy, num_replicas


def test_single_device_strategy_is_default() -> None:
    strategy = get_strategy()
    assert num_replicas() == 1
    assert num_replicas("single") == 1
    assert "OneDeviceStrategy" in type(strategy).__name__


def test_mirrored_strategy_resolves_on_cpu() -> None:
    # One CPU means one replica: the code path is real, CI stays green.
    assert num_replicas("mirrored") >= 1


def test_rejects_unknown_strategy() -> None:
    with pytest.raises(ValueError, match="unknown strategy"):
        get_strategy("multiworker")
