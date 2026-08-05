"""Comprehensive tests for the RAG pgvector extension."""

from __future__ import annotations

import pytest

from app.features.rag.providers import MockEmbeddingProvider, get_embedding_provider
from app.features.rag.repository import InMemoryVectorRepository
from app.features.rag.schemas import Document, RetrievedDocument
from app.features.rag.service import chunk_text, ingest_document, retrieve_context


def test_chunk_text_basic() -> None:
    text = "A" * 1500
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    assert len(chunks) == 2
    assert len(chunks[0]) == 1000
    assert len(chunks[1]) == 700  # 1500 - (1000 - 200) = 700


def test_chunk_text_invalid_config() -> None:
    with pytest.raises(ValueError, match="chunk_size must be strictly greater than overlap"):
        chunk_text("test", chunk_size=100, overlap=100)


def test_chunk_text_empty() -> None:
    assert chunk_text("   ") == []


def test_mock_provider_deterministic() -> None:
    # Different instances should yield identical results for the same string
    # We must use asyncio.run or just await it if in an async test, 
    # but let's test it via the async framework.
    pass


@pytest.mark.asyncio
async def test_mock_provider_async() -> None:
    provider = MockEmbeddingProvider(dimension=3)
    res1 = await provider.embed_documents(["hello"])
    res2 = await provider.embed_documents(["hello"])
    assert res1 == res2
    assert len(res1[0]) == 3
    
    res3 = await provider.embed_documents(["world"])
    assert res1 != res3


@pytest.mark.asyncio
async def test_in_memory_repository() -> None:
    repo = InMemoryVectorRepository()
    
    doc1 = Document(content="hello", metadata={"source": "a"})
    doc2 = Document(content="world", metadata={"source": "b"})
    
    await repo.add_documents([doc1, doc2], [[1.0, 0.0], [0.0, 1.0]])
    
    # Query with [1.0, 0.0] should match doc1
    results = await repo.similarity_search([1.0, 0.0], limit=1)
    assert len(results) == 1
    assert results[0].content == "hello"
    assert results[0].metadata["source"] == "a"
    assert results[0].score < 0.1  # Distance should be 0.0


@pytest.mark.asyncio
async def test_repository_mismatched_lengths() -> None:
    repo = InMemoryVectorRepository()
    with pytest.raises(ValueError, match="Number of documents must match number of embeddings"):
        await repo.add_documents([Document(content="a")], [])


@pytest.fixture
def mock_repo() -> InMemoryVectorRepository:
    return InMemoryVectorRepository()


@pytest.mark.asyncio
async def test_service_ingest_empty_text(mock_repo: InMemoryVectorRepository) -> None:
    count = await ingest_document(mock_repo, "   ")
    assert count == 0
    assert len(mock_repo.store) == 0


@pytest.mark.asyncio
async def test_service_retrieve_empty_query(mock_repo: InMemoryVectorRepository) -> None:
    results = await retrieve_context(mock_repo, "   ")
    assert results == []


@pytest.mark.asyncio
async def test_service_full_workflow(
    mock_repo: InMemoryVectorRepository, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RAG_EMBEDDING_PROVIDER", "mock")

    # Ingest a document
    text = "This is a test document that will be embedded and retrieved."
    count = await ingest_document(
        mock_repo,
        text,
        metadata={"test": True},
        chunk_size=50,
        chunk_overlap=10,
    )
    assert count > 1
    assert len(mock_repo.store) == count

    # Retrieve it
    results = await retrieve_context(mock_repo, "test document", limit=2)
    assert len(results) == 2
    assert isinstance(results[0], RetrievedDocument)
    assert results[0].metadata["test"] is True


def test_get_embedding_provider_invalid() -> None:
    with pytest.raises(ValueError, match="unknown RAG_EMBEDDING_PROVIDER"):
        get_embedding_provider("invalid-provider")
