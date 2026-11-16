import os
from contextlib import contextmanager
from pathlib import Path
from sqlite3 import Connection, IntegrityError, connect

__all__ = [
    "Connection",
    "IntegrityError",
    "get_conn",
    "get_conn_cm",
    "get_db_path",
    "init_db",
    "migrate_user_table",
]


def get_db_path() -> str:
    db_dir = Path(__file__).resolve().parents[1] / "db"
    db_dir.mkdir(exist_ok=True)
    db_path = str(db_dir / "cryptid.db")
    db_name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    return db_name


def get_conn():
    """Yield a database connection and manage its transaction."""
    conn = connect(get_db_path(), check_same_thread=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


get_conn_cm = contextmanager(get_conn)


def migrate_user_table(conn: Connection) -> None:
    """Add columns introduced after the original user table was created."""
    columns = {row[1] for row in conn.execute("pragma table_info(user)")}
    if "role" not in columns:
        conn.execute(
            "alter table user add column role text not null default 'user'"
        )
    if "disabled" not in columns:
        conn.execute(
            "alter table user add column disabled integer not null default 0"
        )


def init_db():
    """Initialize all database tables."""
    with get_conn_cm() as conn:
        # Explorer
        conn.execute("""
            create table if not exists explorer(
                name text primary key,
                country text,
                description text
            )
        """)

        # Creature
        conn.execute("""
            create table if not exists creature(
                name text primary key,
                country text,
                area text,
                description text,
                aka text
            )
        """)

        # User
        conn.execute(
            """
            create table if not exists user(
                name text primary key,
                hash text not null,
                role text not null default 'user',
                disabled integer not null default 0
            )
            """
        )
        migrate_user_table(conn)

        # xuser
        conn.execute(
            """create table if not exists xuser(name text primary key, hash text)"""
        )
