FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY worker ./worker

RUN uv sync --no-dev

CMD ["uv", "run", "celery", "-A", "worker.celery_app", "worker", "--loglevel=INFO"]
