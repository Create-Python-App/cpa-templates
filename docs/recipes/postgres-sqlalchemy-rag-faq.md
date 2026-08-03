# FAQ: Composing PostgreSQL, SQLAlchemy, and AI Extensions

This FAQ explains how PostgreSQL, `fastapi-sqlalchemy`, and AI extensions such as RAG fit together in CPA templates.

## When should I use the `postgres` extension?

Use the `postgres` extension whenever your project requires a PostgreSQL database. It provides the database infrastructure and should be the single source of PostgreSQL configuration.

## When should I use `fastapi-sqlalchemy`?

Use `fastapi-sqlalchemy` when your FastAPI application needs SQLAlchemy models, sessions, and ORM-based database access.

## When should I use AI/RAG extensions?

Use AI extensions such as `fastapi-rag-pgvector` when your application needs document ingestion, embeddings, and retrieval for AI-powered features.

These extensions build on existing infrastructure rather than replacing it.

## What is the recommended composition?

For an AI application using pgvector, the recommended stack is:

- `postgres`
- `fastapi-sqlalchemy` (when ORM/database models are needed)
- `fastapi-rag-pgvector`

Each extension has a single responsibility and should compose with the others.

## What should contributors NOT re-implement?

When building AI extensions:

- Do not re-implement PostgreSQL setup already provided by the `postgres` extension.
- Do not duplicate SQLAlchemy integration already provided by `fastapi-sqlalchemy`.
- Do not tightly couple RAG functionality to every AI application template.
- Prefer composing existing extensions instead of duplicating infrastructure.