"""Shared CLI configuration helpers.

Extend this module when commands need env-based settings (API URLs, verbosity).
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from the environment."""

    log_level: str = "INFO"


def load_settings() -> Settings:
    return Settings(log_level=os.environ.get("CLI_LOG_LEVEL", "INFO"))
