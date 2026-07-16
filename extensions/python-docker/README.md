# Docker

Run the API in a container with [uv](https://docs.astral.sh/uv/).

Compose files follow the same convention as [cna-templates](https://github.com/Create-Node-App/cna-templates): **`compose.yml`** (not `docker-compose.yml`).

## Development

```sh
docker compose up --build
```

API: http://localhost:8000/docs

## Production-style run

```sh
docker compose -f compose.yml -f compose.prod.yml up --build -d
```

## Production notes

- Set `DEBUG=false` in `.env`
- Use a process manager or orchestrator for multi-instance deployments
- Add health checks targeting `/ping`
