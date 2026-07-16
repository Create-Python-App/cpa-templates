# Docker

Run the API in a container with [uv](https://docs.astral.sh/uv/).

## Build and run

```sh
docker compose up --build
```

API: http://localhost:8000/docs

## Production notes

- Set `DEBUG=false` in `.env`
- Use a process manager or orchestrator for multi-instance deployments
- Add health checks targeting `/ping`
