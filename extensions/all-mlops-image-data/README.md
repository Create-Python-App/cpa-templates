# all-mlops-image-data

Framework-agnostic image data pack for MLOps starters. Layers synthetic
uint8 NHWC image generation, `[0, 1]` normalization, and schema validation
onto any `mlops-*` template — NumPy only, no Pillow/torch/TF dependency.

## Generated layout

- `data_packs/image.py` — image synthesis, normalization, validator.
- `tests/test_image_data_pack.py` — shape/determinism/range tests.
- `template/pyproject.toml` — partial: `force-include`s `data_packs` into the wheel.
- `docs/IMAGE_DATA_GUIDE.md` — long-form guide, linked from the project docs.

## Usage (generated project)

```python
from data_packs.image import make_images, normalize_images, validate_images

x, y = make_images(n=32, height=16, width=16, channels=1, seed=42)
validate_images(x, y)
x_float = normalize_images(x)
```
