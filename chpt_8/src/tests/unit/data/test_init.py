from sqlalchemy import inspect

from data.db import get_engine, init_db


def test_init_db_creates_tables():
    """init_db creates all expected tables from the ORM metadata."""
    init_db()
    inspector = inspect(get_engine())
    tables = set(inspector.get_table_names())
    assert {"creature", "explorer", "user", "xuser"} <= tables


def test_init_db_user_columns():
    """The user table has all expected columns after initialization."""
    init_db()
    inspector = inspect(get_engine())
    columns = {col["name"] for col in inspector.get_columns("user")}
    assert columns == {"name", "hash", "role", "disabled"}
