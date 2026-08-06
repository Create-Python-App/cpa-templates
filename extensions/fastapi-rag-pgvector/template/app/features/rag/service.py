"""RAG orchestration service."""

from __future__ import annotations

import os
from typing import Any

from app.features.rag.providers import get_embedding_provider
from app.features.rag.repository import VectorRepository
from app.features.rag.schemas import Document, RetrievedDocument


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Basic sliding window character text splitter.

    A production application might replace this with a more sophisticated
    semantic or token-based splitter if required.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    if not text.strip():
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += (chunk_size - overlap)
    return chunks


async def ingest_document(
    repository: VectorRepository,
    text: str,
    metadata: dict[str, Any] | None = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> int:
    """Chunk a document, generate embeddings, and persist them.

    Returns the number of chunks successfully ingested.
    """
    if not text.strip():
        return 0

    if metadata is None:
        metadata = {}

    # 1. Chunk the text
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap)
    if not chunks:
        return 0

    # 2. Generate embeddings
    provider_name = os.environ.get("RAG_EMBEDDING_PROVIDER", "mock")
    provider = get_embedding_provider(provider_name)
    embeddings = await provider.embed_documents(chunks)

    # 3. Create domain schemas
    documents = [
        Document(content=chunk, metadata=metadata)
        for chunk in chunks
    ]

    # 4. Persist to repository
    await repository.add_documents(documents, embeddings)

    return len(chunks)


async def retrieve_context(
    repository: VectorRepository,
    query: str,
    limit: int = 5,
) -> list[RetrievedDocument]:
    """Embed the search query and perform a vector similarity search."""
    if not query.strip():
        return []

    # 1. Generate embedding for the query
    provider_name = os.environ.get("RAG_EMBEDDING_PROVIDER", "mock")
    provider = get_embedding_provider(provider_name)
    embeddings = await provider.embed_documents([query])

    if not embeddings:
        return []

    query_embedding = embeddings[0]

    # 2. Search the repository
    results = await repository.similarity_search(query_embedding, limit=limit)
    return results
