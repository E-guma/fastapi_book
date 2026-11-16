import sqlite3

from data.init import get_conn_cm, init_db


def test_init_db_creates_user_columns():
    with get_conn_cm() as conn:
        columns = {row[1] for row in conn.execute("pragma table_info(user)")}

    assert columns == {"name", "hash", "role", "disabled"}


def test_init_db_migrates_legacy_user_table(monkeypatch, tmp_path):
    db_path = tmp_path / "legacy.db"
    monkeypatch.setenv("CRYPTID_SQLITE_DB", str(db_path))

    conn = sqlite3.connect(db_path)
    conn.execute("create table user(name text primary key, hash text)")
    conn.execute("insert into user values('alice', 'stored-hash')")
    conn.commit()
    conn.close()

    init_db()

    conn = sqlite3.connect(db_path)
    try:
        columns = {row[1] for row in conn.execute("pragma table_info(user)")}
        assert {"name", "hash", "role", "disabled"} <= columns
        row = conn.execute(
            "select name, hash, role, disabled from user"
        ).fetchone()
        assert row == ("alice", "stored-hash", "user", 0)
    finally:
        conn.close()
