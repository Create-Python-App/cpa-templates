"""Tests for DDP launch helpers — fallback behavior only, no process spawn."""

from __future__ import annotations

import pytest

from mlops_pytorch_distributed.launch import (
    dist_config_from_env,
    is_distributed_launch,
    run_distributed,
)


def test_default_config_is_single_process(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RANK", raising=False)
    monkeypatch.delenv("WORLD_SIZE", raising=False)
    assert dist_config_from_env() == {"rank": 0, "world_size": 1, "backend": "gloo"}
    assert is_distributed_launch() is False


def test_torchrun_env_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RANK", "1")
    monkeypatch.setenv("WORLD_SIZE", "4")
    cfg = dist_config_from_env()
    assert (cfg["rank"], cfg["world_size"]) == (1, 4)
    assert is_distributed_launch() is True


def test_world_size_without_rank_is_not_a_launch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Configured multi-process but not actually launched under torchrun:
    # stay on the safe single-process path instead of hanging on rendezvous.
    monkeypatch.delenv("RANK", raising=False)
    monkeypatch.delenv("WORLD_SIZE", raising=False)
    assert is_distributed_launch({"rank": 0, "world_size": 4, "backend": "gloo"}) is False


def test_single_process_runs_fn_directly() -> None:
    assert run_distributed(lambda x, y: x + y, 2, 3, world_size=1) == 5


def test_rejects_bad_world_size() -> None:
    with pytest.raises(ValueError, match="world_size"):
        run_distributed(lambda: None, world_size=0)
