"""Database engine and session lifecycle."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from data.models import Base

load_dotenv()

__all__ = [
    "Session",
    "get_db",
    "get_db_cm",
    "get_db_path",
    "init_db",
]


def get_db_path() -> str:
    """Return the path to the SQLite database file."""
    db_dir = Path(__file__).resolve().parents[1] / "db"
    db_dir.mkdir(exist_ok=True)
    db_path = str(db_dir / "cryptid.db")
    return os.getenv("CRYPTID_SQLITE_DB", db_path)


_engine: Engine | None = None
_db_path: str | None = None


def get_engine() -> Engine:
    """Return the SQLAlchemy engine, recreating it if the DB path changed."""
    global _engine, _db_path
    path = get_db_path()
    if _engine is None or _db_path != path:
        _engine = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
        _db_path = path
    return _engine


def get_db() -> Iterator[Session]:
    """Yield a Session and manage its transaction.

    Intended for use as a FastAPI dependency (``Depends(get_db)``) or as a
    context manager via :data:`get_db_cm`.
    """
    engine = get_engine()
    with Session(engine) as session, session.begin():
        yield session


get_db_cm = contextmanager(get_db)


def init_db() -> None:
    """Create all database tables from the ORM metadata."""
    Base.metadata.create_all(bind=get_engine())
