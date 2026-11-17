import os
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

__all__ = [
    "Base",
    "Session",
    "get_db",
    "get_db_cm",
    "get_db_path",
    "init_db",
]


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db_path() -> str:
    """Return the path to the SQLite database file."""
    db_dir = Path(__file__).resolve().parents[1] / "db"
    db_dir.mkdir(exist_ok=True)
    db_path = str(db_dir / "cryptid.db")
    db_name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    return db_name


_engine = None
_db_path = None


def get_engine():
    """Return the SQLAlchemy engine, recreating it if the DB path changed."""
    global _engine, _db_path
    path = get_db_path()
    if _engine is None or _db_path != path:
        _engine = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
        _db_path = path
    return _engine


def get_db():
    """Yield a SQLAlchemy Session and manage its transaction.

    Intended for use as a FastAPI dependency (``Depends(get_db)``) or as a
    context manager via :data:`get_db_cm`.
    """
    engine = get_engine()
    db = Session(engine)
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


get_db_cm = contextmanager(get_db)


def init_db():
    """Initialize all database tables from the ORM metadata."""
    Base.metadata.create_all(bind=get_engine())
