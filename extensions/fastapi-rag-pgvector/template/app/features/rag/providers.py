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
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        self.dimension = dimension

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return deterministic fake embeddings based on the text hash."""
        if self.dimension <= 0:
            raise ValueError("dimension must be positive")
        results = []
        for text in texts:
            vec: list[float] = []
            for i in range(self.dimension):
                # Deterministic per-dimension value derived from SHA-256
                digest = hashlib.sha256(f"{text}:{i}".encode("utf-8")).digest()
                value = int.from_bytes(digest[:4], "big") / (2**32)
                vec.append(value)
            results.append(vec)
        return results


def get_embedding_provider(name: str) -> EmbeddingProvider:
    """Factory function to get the configured embedding provider."""
    if name == "mock":
        return MockEmbeddingProvider()
    raise ValueError(f"unknown RAG_EMBEDDING_PROVIDER: {name!r}")
