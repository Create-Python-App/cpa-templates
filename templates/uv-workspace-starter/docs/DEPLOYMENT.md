# Deployment

## Build all members

```bash
uv build --all-packages
```

See [RELEASING.md](RELEASING.md) for versioning and publishing individual
distributions.

## Deployable apps

Treat `apps/*` as the units you containerize or ship:

- CLI apps → console scripts / wheels (see member README)
- HTTP / worker apps → use the matching stack Docker extension when scaffolding
  that member's layout

## Checklist

- [ ] Root lockfile (`uv.lock`) committed
- [ ] Each publishable member has a clear version policy
- [ ] CI runs lint + types + tests across the workspace
- [ ] Secrets never committed; per-app `.env.example` only
