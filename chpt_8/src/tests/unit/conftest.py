import pytest

from data.init import init_db


@pytest.fixture(autouse=True)
def db_tables(monkeypatch, tmp_path):
    """Create fresh database tables for each test"""
    print(str(tmp_path.resolve()))
    monkeypatch.setenv("CRYPTID_SQLITE_DB", str(tmp_path / "test.db"))
    init_db()
