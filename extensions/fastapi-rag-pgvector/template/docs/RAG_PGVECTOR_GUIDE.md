# RAG pgvector Guide

This extension provides a foundational Retrieval-Augmented Generation (RAG) data layer using PostgreSQL and `pgvector`. It is designed to be lightweight, avoiding heavy frameworks like LangChain in favor of raw performance and transparency.

## Architecture

*   **`app.features.rag.schemas`**: Pydantic models defining the Input/Output boundaries (`Document`, `RetrievedDocument`).
*   **`app.features.rag.providers`**: A factory for embedding models. Supports switching between providers without modifying your business logic.
*   **`app.features.rag.repository`**: Handles database interactions using `psycopg` and `pgvector`. It assumes a valid `DATABASE_URL` is configured.
*   **`app.features.rag.service`**: The business logic orchestration layer. It handles text chunking, calls the embedding provider, and communicates with the repository.

## Configuration

Set the following environment variables:

*   `DATABASE_URL`: Connection string for PostgreSQL (must have pgvector enabled).
*   `RAG_EMBEDDING_PROVIDER`: The embedding provider to use (default: `mock`). Supported: `mock`.

## Database Schema & Migrations

This extension assumes the database schema exists. It **does not** automatically create tables.
You must create the following table (using Alembic or raw SQL):

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE rag_documents (
    id bigserial PRIMARY KEY,
    content text NOT NULL,
    metadata jsonb NOT NULL,
    embedding vector(1536)
);
-- For cosine similarity search, create an index:
-- CREATE INDEX ON rag_documents USING ivfflat (embedding vector_cosine_ops);
```
*(If using `fastapi-sqlalchemy`, add a `Document` model and generate a migration. Ensure the `vector` column dimension matches `EMBEDDING_DIMENSION` (1536).)*

## Usage Example

```python
from app.features.rag.service import ingest_document, retrieve_context

# Ingesting data
await ingest_document(
    text="CPA is a great framework for building Python applications.",
    metadata={"source": "docs", "author": "admin"}
)

# Semantic Search
results = await retrieve_context(query="What is CPA?", limit=3)
for doc in results:
    print(doc.content, doc.score)
```

## Troubleshooting

- **`psycopg.OperationalError`**: Ensure `DATABASE_URL` is correct and PostgreSQL is running.
- **`ValueError: unknown RAG_EMBEDDING_PROVIDER`**: You set `RAG_EMBEDDING_PROVIDER` to an unimplemented provider. Supported: `mock` (or others you implement).
- **`relation "rag_documents" does not exist`**: You did not create the schema. Read the 'Database Schema' section above.

