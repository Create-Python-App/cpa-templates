# mlops-pytorch-distributed

DDP/torchrun launch helpers for PyTorch starters (`torch.distributed`
gloo — no new dependencies). Single-process fallback is the default.

## Generated layout

- `mlops_pytorch_distributed/launch.py` — env detection, `run_distributed()`.
- `template/pyproject.toml` — partial: `force-include`s the helpers into
  the wheel.
- `tests/test_pytorch_distributed.py` — fallback + env-detection tests
  (no process spawn in CI).
- `docs/DISTRIBUTED_TRAINING_GUIDE.md` — local execution, cluster/GPU notes.

## Usage (generated project)

```python
from mlops_pytorch_distributed.launch import is_distributed_launch

if not is_distributed_launch():
    train_shard()  # local default
```
