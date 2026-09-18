"""Schemas for the RAG feature."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A document to be indexed for retrieval."""

    content: str = Field(..., description="The raw text content of the document.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional key-value metadata."
    )


class RetrievedDocument(Document):
    """A document retrieved from the vector store with its similarity score."""

    score: float = Field(
        ...,
        description="Similarity score (e.g. cosine distance, where lower is better).",
    )
