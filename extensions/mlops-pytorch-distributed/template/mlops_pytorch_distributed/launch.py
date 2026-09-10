"""Config-driven distributed launch for PyTorch starters (DDP/torchrun).

Single-process execution is the default and always works: distributed code
paths activate only when ``world_size > 1`` is configured AND the process
was launched under ``torchrun`` (``RANK``/``WORLD_SIZE`` env present).
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import torch.distributed as dist

_BACKEND = "gloo"  # CPU-safe; NCCL only via explicit cluster configuration.


def dist_config_from_env() -> dict[str, Any]:
    """Read torchrun env into a plain config dict (rank 0 / world 1 default)."""
    return {
        "rank": int(os.environ.get("RANK", "0")),
        "world_size": int(os.environ.get("WORLD_SIZE", "1")),
        "backend": os.environ.get("DIST_BACKEND", _BACKEND),
    }


def is_distributed_launch(config: dict[str, Any] | None = None) -> bool:
    """True only when a real multi-process launch is configured AND present."""
    cfg = config or dist_config_from_env()
    return bool(cfg["world_size"] > 1 and "RANK" in os.environ)


def run_distributed(
    fn: Callable[..., Any],
    *args: Any,
    world_size: int = 1,
    backend: str = _BACKEND,
) -> Any:
    """Run ``fn(*args)`` once (``world_size == 1``, the CI-safe fallback) or
    once per process via ``torch.multiprocessing.spawn`` (cluster path)."""
    if world_size < 1:
        raise ValueError(f"world_size must be >= 1, got {world_size}")
    if world_size == 1:
        return fn(*args)
    import torch.multiprocessing as mp

    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", "29517")
    return mp.spawn(
        _spawn_entry, args=(world_size, fn, args, backend), nprocs=world_size
    )


def _spawn_entry(
    rank: int,
    world_size: int,
    fn: Callable[..., Any],
    args: tuple[Any, ...],
    backend: str,
) -> Any:
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)
    try:
        return fn(*args)
    finally:
        dist.destroy_process_group()
