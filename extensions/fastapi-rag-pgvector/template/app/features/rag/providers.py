"""Embedding model provider factory."""

from __future__ import annotations

import abc
import hashlib


class EmbeddingProvider(abc.ABC):
    """Abstract base class for embedding providers."""

    @abc.abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Convert a list of strings into a list of embedding vectors."""
        pass


class MockEmbeddingProvider(EmbeddingProvider):
    """A deterministic fake embedding provider for tests."""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return deterministic fake embeddings based on the text hash."""
        results = []
        for text in texts:
            # Generate a stable float between 0 and 1 based on the text
            seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
            value = (seed % 100) / 100.0

            vec = [0.0] * self.dimension
            vec[0] = value
            results.append(vec)
        return results


def get_embedding_provider(name: str) -> EmbeddingProvider:
    """Factory function to get the configured embedding provider."""
    if name == "mock":
        return MockEmbeddingProvider()
    raise ValueError(f"unknown RAG_EMBEDDING_PROVIDER: {name!r}")
