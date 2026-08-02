# Contributing

1. Add or modify a pipeline step under `data/` or `models/`, implementing
   `BaseStep` from `pipeline/base.py`.
2. Register it in `pipeline/steps_registry.py`.
3. Add or update its config section in `config.py` and `configs/default.yaml`.
4. Add tests — see `docs/TESTING_GUIDE.md`.
5. Run `uv run ruff check .`, `uv run mypy .`, `uv run pyright`, and
   `uv run pytest` before committing.

See `docs/MLOPS_PIPELINE.md` for the full pipeline contract.
