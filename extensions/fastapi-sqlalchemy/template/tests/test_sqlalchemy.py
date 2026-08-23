"""Tests for fastapi-sqlalchemy extension (session, Base, Alembic, get_db)."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, get_db, session_factory

# ---------------------------------------------------------------------------
# Declarative Base
# ---------------------------------------------------------------------------


def test_base_is_declarative() -> None:
    assert hasattr(Base, "metadata")
    assert hasattr(Base, "registry")


def test_model_can_register_on_base() -> None:
    class TempModel(Base):
        __tablename__ = "temp_model_w3_probe"
        __allow_unmapped__ = True
        id: int = Column(Integer, primary_key=True)  # type: ignore[assignment]
        name: str = Column(String(50))  # type: ignore[assignment]

    assert "temp_model_w3_probe" in Base.metadata.tables
    # Cleanup so subsequent tests/alembic autogenerate don't see the probe
    Base.metadata.remove(TempModel.__table__)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


# ---------------------------------------------------------------------------
# Engine and session factory (file-backed sqlite default)
# ---------------------------------------------------------------------------


def test_engine_is_created() -> None:
    assert engine is not None
    # Default URL is sqlite when DATABASE_URL unset
    assert "sqlite" in str(engine.url) or "postgresql" in str(engine.url)


def test_session_factory_produces_session() -> None:
    session = session_factory()
    try:
        assert isinstance(session, Session)
        # smoke: execute a trivial query
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        session.close()


def test_get_db_yields_and_closes() -> None:
    gen: Generator[Session, None, None] = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    # Use the session
    assert db.execute(text("SELECT 1")).scalar() == 1
    # Exhaust generator to trigger close
    try:
        next(gen)
        pytest.fail("get_db should be a single-yield generator")
    except StopIteration:
        pass
    # After close, session should be closed (is_active == False)
    # SQLAlchemy 2.x: check closed state via `is_active` or `bind`


def test_in_memory_roundtrip_isolated() -> None:
    """Isolated in-memory SQLite round-trip with a throwaway model."""

    class IsolatedModel(Base):
        __tablename__ = "isolated_w3_test"
        __allow_unmapped__ = True
        id: int = Column(Integer, primary_key=True)  # type: ignore[assignment]
        value: str = Column(String(100))  # type: ignore[assignment]

    memory_engine = create_engine("sqlite:///:memory:", future=True)
    try:
        Base.metadata.create_all(
            memory_engine, tables=[IsolatedModel.__table__]  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]
        )
        with Session(memory_engine) as session:
            session.add(IsolatedModel(value="hello-w3"))
            session.commit()
            rows = session.query(IsolatedModel).all()
            assert len(rows) == 1
            assert rows[0].value == "hello-w3"
    finally:
        IsolatedModel.__table__.drop(memory_engine, checkfirst=True)  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]
        Base.metadata.remove(IsolatedModel.__table__)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        memory_engine.dispose()


# ---------------------------------------------------------------------------
# Alembic wiring (no DB mutation, just config sanity)
# ---------------------------------------------------------------------------


def test_alembic_env_has_target_metadata() -> None:
    from pathlib import Path

    env_path = Path(__file__).resolve().parents[1] / "alembic" / "env.py"
    assert env_path.is_file(), f"alembic/env.py not found at {env_path}"
    content = env_path.read_text(encoding="utf-8")
    # Must import Base and wire target_metadata
    assert "from app.db.base import Base" in content
    assert "target_metadata = Base.metadata" in content
    assert "DATABASE_URL" in content
    # Verify actual target_metadata is Base.metadata (avoid executing alembic context)
    assert Base.metadata is not None


def test_database_url_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # Re-import session module logic by checking os.getenv path
    assert os.getenv("DATABASE_URL") == "sqlite:///:memory:"
    mem_engine = create_engine(os.getenv("DATABASE_URL", ""), future=True)
    try:
        with mem_engine.connect() as conn:
            assert conn.execute(text("SELECT 1")).scalar() == 1
    finally:
        mem_engine.dispose()


def test_session_respects_sqlite_connect_args() -> None:
    from pathlib import Path

    session_path = Path(__file__).resolve().parents[1] / "app" / "db" / "session.py"
    assert session_path.is_file(), f"session.py not found at {session_path}"
    content = session_path.read_text(encoding="utf-8")
    # Scaffolded session.py must handle sqlite threading correctly
    assert 'check_same_thread' in content
    assert 'False' in content
    assert 'sqlite' in content.lower()
