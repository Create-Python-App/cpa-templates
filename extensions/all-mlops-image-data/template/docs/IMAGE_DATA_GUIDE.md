# Image Data Pack

Framework-agnostic image helpers for MLOps starters
(`data_packs/image.py`, NumPy only — no Pillow/torch/TF dependency).

## What it adds

- `make_images()` — deterministic two-pattern uint8 NHWC images plus binary
  labels, shuffled.
- `normalize_images()` — uint8 `[0, 255]` to float32 `[0, 1]` (idempotent).
- `validate_images()` — NHWC/dtype/range/count schema rules.

## Usage

```python
from data_packs.image import make_images, normalize_images, validate_images

x, y = make_images(n=32, height=16, width=16, channels=1, seed=42)
validate_images(x, y)
x_float = normalize_images(x)
```

## Configuration

Pure function arguments only — no environment variables.

## Verification

```bash
uv run pytest tests/test_image_data_pack.py -v
```

Covers shapes/dtypes, determinism, unit-range scaling + idempotence, and
every validation rejection.

## Troubleshooting

- `ValueError: float images must be in [0, 1]` — run `normalize_images`
  first, or scale your own loader output.
- Framework image loaders (torchvision/tf.data) expect their own layouts —
  this pack covers synthetic/NumPy input; adapt channels/scales at the
  framework boundary.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (synthetic/fixture-only policy).
