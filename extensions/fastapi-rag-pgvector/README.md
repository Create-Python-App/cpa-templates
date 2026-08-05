# RAG pgvector Extension

Adds semantic search and document retrieval infrastructure using `pgvector` for FastAPI applications.

## What this adds

This extension provides a generic backend service for chunking, embedding, and semantic similarity search. It serves as the foundational data layer for AI applications (like Chatbots, Agentic workflows, or context-aware search).

## Coupling truth

- **Stack:** FastAPI (`fastapi-backend`).
- **Database:** PostgreSQL with `pgvector` enabled.
- **ORM Independence:** This extension utilizes `langchain-postgres` and connects via standard database URIs. It is fully compatible with, but does not strictly require, `fastapi-sqlalchemy`.
- **UI Independence:** This extension does not add a chat UI, endpoints, or LLM generation logic. It strictly provides retrieval services that other features can import.

## Composition

For a complete stack, compose this with:
- `fastapi-sqlalchemy` (Recommended if you want standard ORM schema management)
- `postgres` (Provides the Docker Compose infrastructure with pgvector)
- `fastapi-ai-chat` (Provides the user-facing generation endpoints)

Example:
```sh
uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons postgres fastapi-sqlalchemy fastapi-rag-pgvector \
  --yes
```
