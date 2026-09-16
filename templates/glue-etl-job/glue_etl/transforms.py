"""Pure-Python transform helpers shared by the Glue job script and unit tests.

These functions operate on plain dictionaries so they can be tested without a
Spark or Glue runtime. The Glue script in ``jobs/`` applies them row-wise and
is responsible for all Spark I/O (reads, writes, Data Catalog updates).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Strip whitespace from string values and drop ``None`` entries."""
    normalized: dict[str, Any] = {}
    for key, value in record.items():
        if value is None:
            continue
        normalized[key] = value.strip() if isinstance(value, str) else value
    return normalized


def drop_records_missing_keys(
    records: list[dict[str, Any]], required_keys: list[str]
) -> list[dict[str, Any]]:
    """Keep only records that carry every key in ``required_keys``."""
    return [
        record for record in records if all(record.get(key) is not None for key in required_keys)
    ]


def with_ingestion_date(
    record: dict[str, Any], ingested_at: datetime | None = None
) -> dict[str, Any]:
    """Return a copy of ``record`` stamped with an ``ingestion_date`` (UTC, ``YYYY-MM-DD``)."""
    stamped = dict(record)
    moment = ingested_at or datetime.now(UTC)
    stamped["ingestion_date"] = moment.strftime("%Y-%m-%d")
    return stamped


def clean_batch(
    records: list[dict[str, Any]], required_keys: list[str], ingested_at: datetime | None = None
) -> list[dict[str, Any]]:
    """Normalize, filter, and stamp a batch of raw source records."""
    cleaned: list[dict[str, Any]] = []
    for record in drop_records_missing_keys(records, required_keys):
        cleaned.append(with_ingestion_date(normalize_record(record), ingested_at))
    return cleaned
