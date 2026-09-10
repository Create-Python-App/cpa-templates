"""Shared step interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

StepContext = dict[str, Any]


class BaseStep(ABC):
    name: str

    def validate(self, context: StepContext) -> None:
        """Optional pre-flight checks."""
        return None

    @abstractmethod
    def run(self, context: StepContext) -> StepContext:
        raise NotImplementedError
