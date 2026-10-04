# Template quality (M1)

Track the maturity bar for all catalog templates. Formal M1 checklists live
next to templates as `QUALITY.md`; templates without that file remain pre-M1
until their acceptance criteria are reviewed and checked in.

## Coverage summary

| Template | Local `QUALITY.md` | M1 bar | Notes |
|---|---:|---:|---|
| `fastapi-starter` | Yes | Defined | [Checklist](../templates/fastapi-starter/QUALITY.md) |
| `django-api` | Yes | Defined | [Checklist](../templates/django-api/QUALITY.md) |
| `mlops-sklearn-starter` | Yes | Defined | [Checklist](../templates/mlops-sklearn-starter/QUALITY.md), defined by [#223](https://github.com/Create-Python-App/cpa-templates/issues/223) |
| `mlops-pytorch-starter` | Yes | Defined | [Checklist](../templates/mlops-pytorch-starter/QUALITY.md), defined by [#223](https://github.com/Create-Python-App/cpa-templates/issues/223) |
| `mlops-tensorflow-starter` | Yes | Defined | [Checklist](../templates/mlops-tensorflow-starter/QUALITY.md), defined by [#223](https://github.com/Create-Python-App/cpa-templates/issues/223) |
| `celery-worker` | No | Pre-M1 | Interim criteria below |
| `cli-starter` | No | Pre-M1 | Interim criteria below |
| `glue-etl-job` | No | Pre-M1 | Newest template; M1 bar still needs to be defined |
| `uv-workspace-starter` | No | Pre-M1 | Interim criteria below |

The five defined bars should remain synchronized with their local checklists.
The four pre-M1 templates must not be described as formally mature until a
reviewed `QUALITY.md` is added. `glue-etl-job`, added in [#230](https://github.com/Create-Python-App/cpa-templates/pull/230), is the newest addition and is the next priority for a formal M1 definition.

## Pre-M1 expectations

These are interim acceptance expectations, not formal M1 bars. They give
maintainers a minimum review surface while each template's local checklist is
being authored.

### `celery-worker`

- README documents `uv sync`, worker startup, test, lint, and type-check commands.
- A smoke test covers the worker application or task registration without
  requiring a live broker or Redis service.
- `.env.example` documents broker and result-backend settings.
- CPU/local tests pass with `uv sync`, Ruff, pytest, and the configured type
  checker.
- Compatible `celery-docker`, `flower-docker`, and infrastructure extensions
  are documented, including any mutually exclusive Compose ownership.

### `cli-starter`

- README documents installation, the generated command, help output, and test,
  lint, and type-check commands.
- A pytest smoke test invokes the CLI and covers the default command path plus
  an invalid-input or error path.
- `cpa.config.json` variables produce a runnable command after scaffolding.
- `uv sync`, Ruff, pytest, and the configured type checkers pass after scaffold.

### `glue-etl-job`

- README documents local setup, the ETL entry point, test, lint, and type-check
  commands, and distinguishes local execution from AWS Glue deployment.
- Tests cover transformation logic with fixtures and do not require AWS
  credentials, a live Glue job, or network access.
- `.env.example` and deployment documentation identify AWS region, catalog,
  bucket, and job configuration without embedding credentials.
- The PySpark/Glue runtime boundary and Terraform deployment path are clearly
  documented, with `uv sync` and local quality checks passing after scaffold.
- A future `QUALITY.md` should define the supported Glue/Python runtime matrix
  and the minimum deployment smoke test.

### `uv-workspace-starter`

- README documents workspace creation, member discovery, test, lint, and type-
  check commands.
- A smoke test covers at least the example package and app after workspace
  scaffolding.
- Workspace members use a consistent Python version and the shared Ruff,
  mypy, and pyright configuration remains valid from the workspace root.
- `uv sync`, workspace tests, Ruff, and type checking pass without relying on
  undeclared member-local setup.

## AI/ML taxonomy

The three MLOps starters use the AI/ML template taxonomy and composition rules
defined in [AUTHORING.md](./AUTHORING.md#ai-ml-catalog) and
[AI_ML_AUTHORING.md](./AI_ML_AUTHORING.md). Keep their formal checklists
aligned with the CPU-first testing rule, framework-specific serving contract,
and compatible modality/distributed extension slots documented there. Do not
create a new AI/ML template type when an extension is the appropriate optional
capability.

## Verification

```bash
# L1 alone (templates are auto-included from templates.json)
python scripts/ci/generate-matrix.py --layer templates

# Manual scaffold check (uses published CLI via uvx)
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/fastapi-starter"
```

For a new or newly formalized template, replace the `subdir` value with the
template under review and run its generated project's documented checks. The
profile validator is also useful for confirming that registered template and
extension combinations remain valid:

```bash
python scripts/ci/generate-matrix.py --layer validate-profiles
```

## Related issues

- cpa-templates#49 — FastAPI M1 maturity checklist
- cpa-templates#223 — M1 quality bar for the MLOps starters
- cpa-templates#230 — `glue-etl-job` template addition
- cpa-templates#233 — M1 quality coverage for all catalog templates
- cpa-templates#46 / #47 — layered CI trust
- cpa-templates#57 — typed tooling unified into `fastapi-starter`
