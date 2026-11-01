import os
from pathlib import Path
from contextlib import contextmanager
from sqlite3 import Connection, connect, IntegrityError

db_dir = Path(__file__).resolve().parents[1] / "db"
db_dir.mkdir(exist_ok=True)
db_path = str(db_dir / "cryptid.db")
db_name = os.getenv("CRYPTID_SQLITE_DB", db_path)


def get_conn():
    """Setup Database Connection"""
    conn = connect(db_name, check_same_thread=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


get_conn_cm = contextmanager(get_conn)


def init_db():
    """Initialize all database tables."""
    with get_conn_cm() as conn:
        # Create Explorer table
        conn.execute("""
            create table if not exists explorer(
                name text primary key,
                country text,
                description text
            )
        """)

        # Create Creature table
        conn.execute("""
            create table if not exists creature(
                name text primary key,
                country text,
                area text,
                description text,
                aka text
            )
        """)
