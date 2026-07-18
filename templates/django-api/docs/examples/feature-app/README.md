# Feature app scaffold (copy into `apps/`)

This directory is documentation — it is **not** an installed Django app.

1. Copy `docs/examples/feature-app/` → `apps/<feature_name>/`.
2. Rename the app config `name` in `apps.py` to `apps.<feature_name>`.
3. Fix imports from `apps.<feature_name>...`.
4. Add the app to `INSTALLED_APPS` in `config/settings.py`.
5. Include its urls from `config/urls.py` under `API_PREFIX`.
6. Add tests under `tests/`.
