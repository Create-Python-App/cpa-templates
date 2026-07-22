# Common MLOps template contract

Shared backbone for `mlops-sklearn-starter`, `mlops-pytorch-starter`, and
`mlops-tensorflow-starter`. Implement this contract before adding framework
templates ([#83](https://github.com/Create-Python-App/cpa-templates/issues/83)).

## Layout

```text
src/<package>/
  config.py          # typed settings / YAML loader
  steps/             # BaseStep implementations
  training/          # train entrypoints
  serving/           # predict / batch score
configs/             # YAML experiment configs
tests/
docs/                # CPA required docs suite
.env.example
```

Package name defaults to the project slug (e.g. `mlops_sklearn`).

## `BaseStep`

Every pipeline step implements:

- `name: str`
- `run(self, context: dict) -> dict` mutating/returning a context mapping
- Optional `validate(self, context) -> None`

Steps are composed in order from YAML (`steps:` list).

## Config

- YAML under `configs/` is the source of truth for experiments.
- Typed Python model loads YAML (pydantic v2).
- Local sample data only: tiny generated or fixture files under `tests/fixtures/` or
  generated in-process. No external dataset downloads in default tests.

## MLflow policy

- Local/offline tracking by default (`MLFLOW_TRACKING_URI=sqlite:///./mlflow.db`).
- Remote tracking is opt-in via env placeholders only.
- Tests must not require a remote MLflow server.

## Dependencies

- CPU-first defaults; no CUDA wheels in the base template.
- Framework pins live in the framework template; shared tooling is uv + Ruff + pytest +
  pyright/mypy consistent with CPA.

## Out of scope for base templates

- GitHub Actions CI/CT/CD → `all-mlops-github-actions`
- Distributed training → framework-specific extensions
- Large modality packs → `all-mlops-*-data` extensions

## M1 checklist (from CNA maturity lessons)

Every MLOps template must ship:

- [ ] `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.env.example`, `.gitignore`
- [ ] Full `docs/` suite (README, PROJECT_STRUCTURE, CONFIGURATION, TESTING_GUIDE,
      DEPLOYMENT, TYPING)
- [ ] Real tests: config load, train smoke, predict smoke
- [ ] No network/API credentials required for `pytest`
- [ ] Registered in `templates.json` with type + `mlops` category
