"""Vector repository interface and implementations."""

from __future__ import annotations

import abc
import json
import math
import os

import psycopg
from pgvector.psycopg import register_vector

from app.features.rag.schemas import Document, RetrievedDocument


class VectorRepository(abc.ABC):
    """Abstract base class for vector storage and retrieval."""

    @abc.abstractmethod
    async def add_documents(
        self, documents: list[Document], embeddings: list[list[float]]
    ) -> None:
        """Persist documents and their corresponding embeddings."""
        pass

    @abc.abstractmethod
    async def similarity_search(
        self, query_embedding: list[float], limit: int = 5
    ) -> list[RetrievedDocument]:
        """Retrieve documents similar to the query embedding."""
        pass


class PostgresVectorRepository(VectorRepository):
    """PostgreSQL implementation using pgvector."""

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

    async def add_documents(
        self, documents: list[Document], embeddings: list[list[float]]
    ) -> None:
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings.")

        async with await psycopg.AsyncConnection.connect(self.database_url) as conn:
            await register_vector(conn)
            async with conn.cursor() as cur:
                for doc, emb in zip(documents, embeddings, strict=True):
                    query = (
                        "INSERT INTO rag_documents (content, metadata, embedding) "
                        "VALUES (%s, %s, %s)"
                    )  # noqa: E501
                    await cur.execute(query, (doc.content, json.dumps(doc.metadata), emb))
            await conn.commit()

    async def similarity_search(
        self, query_embedding: list[float], limit: int = 5
    ) -> list[RetrievedDocument]:
        results: list[RetrievedDocument] = []
        async with await psycopg.AsyncConnection.connect(self.database_url) as conn:
            await register_vector(conn)
            async with conn.cursor() as cur:
                # <=> is cosine distance in pgvector
                await cur.execute(
                    """
                    SELECT content, metadata, embedding <=> %s AS distance
                    FROM rag_documents
                    ORDER BY distance
                    LIMIT %s
                    """,
                    (query_embedding, limit),
                )
                rows = await cur.fetchall()
                for row in rows:
                    content, metadata_json, distance = row
                    results.append(
                        RetrievedDocument(
                            content=content,
                            metadata=metadata_json if isinstance(metadata_json, dict) else {},
                            score=float(distance),
                        )
                    )
        return results


class InMemoryVectorRepository(VectorRepository):
    """Fake repository for testing without PostgreSQL."""

    def __init__(self) -> None:
        self.store: list[tuple[Document, list[float]]] = []

    async def add_documents(
        self, documents: list[Document], embeddings: list[list[float]]
    ) -> None:
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings.")
        for doc, emb in zip(documents, embeddings, strict=True):
            self.store.append((doc, emb))

    def _cosine_distance(self, a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 1.0
        dot = sum(x * y for x, y in zip(a, b, strict=True))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 1.0
        similarity = dot / (norm_a * norm_b)
        return 1.0 - similarity  # Distance

    async def similarity_search(
        self, query_embedding: list[float], limit: int = 5
    ) -> list[RetrievedDocument]:
        scored_docs = []
        for doc, emb in self.store:
            distance = self._cosine_distance(query_embedding, emb)
            scored_docs.append(
                RetrievedDocument(content=doc.content, metadata=doc.metadata, score=distance)
            )

        # Sort by distance (lower is better)
        scored_docs.sort(key=lambda x: x.score)
        return scored_docs[:limit]
