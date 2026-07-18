# Deployment

## Console script

After `uv sync` / install, the scaffold exposes:

```bash
uv run my-cli --help
```

(`my-cli` is the default `commandName`; rename via scaffold options.)

## Packaging

```bash
uv build
# publish wheel/sdist to your index when ready
```

## Containers (optional)

Pure CLIs often ship as wheels or standalone binaries (PyInstaller / shiv).
If you need a container, write a thin Dockerfile that installs the wheel and
sets `ENTRYPOINT` to the console script — do not reuse FastAPI Docker overlays.

## Checklist

- [ ] Console script name stable for users
- [ ] `--version` matches package version
- [ ] CI runs `pytest` + `ruff`
- [ ] README documents install for end users
