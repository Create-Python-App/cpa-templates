# Distributed Training (PyTorch)

Config-driven DDP/torchrun launch for PyTorch starters
(`mlops_pytorch_distributed/`, `torch.distributed` gloo — no new
dependencies).

## What it adds

- `dist_config_from_env()` / `is_distributed_launch()` — torchrun env
  detection with rank-0/world-1 defaults.
- `run_distributed(fn, *args, world_size=1)` — direct call on the
  single-process fallback; `torch.multiprocessing.spawn` (gloo, localhost)
  when `world_size > 1`.

## Usage

```python
from mlops_pytorch_distributed.launch import is_distributed_launch, run_distributed

def train_shard() -> dict:
    ...

if is_distributed_launch():
    run_distributed(train_shard, world_size=int(os.environ["WORLD_SIZE"]))
else:
    train_shard()  # local default
```

## Local execution

`world_size=1` (the default) never spawns processes and never initializes
a process group — this is the CI path. Multi-process smoke on one machine:

```bash
WORLD_SIZE=2 python -c "from mlops_pytorch_distributed.launch import run_distributed; ..."
```

or real `torchrun --nproc_per_node=2 train.py` once the training entry
reads `RANK`/`WORLD_SIZE`.

## Cluster / GPU runner notes

- Switch `backend` from `gloo` to `nccl` on CUDA hosts.
- Aggregate metrics across ranks (mean loss/accuracy) before MLflow
  logging; log once from rank 0 to avoid duplicate runs.
- Missing GPUs: DDP still works on CPU via gloo — slowness, not failure,
  is the symptom. Process launch failures almost always mean
  `MASTER_ADDR`/`MASTER_PORT` mismatch or a blocked port.

## Troubleshooting

- Hang on init — `is_distributed_launch()` guards this: a configured
  `world_size > 1` without torchrun env stays single-process by design.
- `ValueError: world_size must be >= 1` — check config parsing.
- Port collision on 29517 — set `MASTER_PORT` explicitly per run.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (GPU/distributed outside default CI).
- PyTorch DDP + torchrun docs.
