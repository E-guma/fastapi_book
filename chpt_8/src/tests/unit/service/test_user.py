from data import user as data
from data.db import get_db_cm
from model.user import User, UserCreate, UserInDB
from service import user as service
from service.auth import verify_password


def test_create_hashes_password():
    with get_db_cm() as conn:
        created = service.create(
            conn,
            UserCreate(name="alice", password="password123"),
        )
        stored = data.get_one(conn, "alice")

    assert created == User(name="alice")
    assert stored.hash != "password123"
    assert verify_password("password123", stored.hash)
    assert "password" not in stored.model_dump()


def test_create_forces_safe_defaults():
    payload = UserCreate(
        name="alice",
        password="password123",
        role="admin",
        disabled=True,
    )
    with get_db_cm() as conn:
        created = service.create(conn, payload)
        stored = data.get_one(conn, "alice")

    assert created.role == "user"
    assert created.disabled is False
    assert stored.role == "user"
    assert stored.disabled is False


def test_get_one_hides_hash():
    with get_db_cm() as conn:
        service.create(conn, UserCreate(name="alice", password="password123"))
        result = service.get_one(conn, "alice")

    assert type(result) is User
    assert not isinstance(result, UserInDB)
    assert not hasattr(result, "hash")


def test_modify_preserves_hash():
    with get_db_cm() as conn:
        service.create(conn, UserCreate(name="alice", password="password123"))
        updated = service.modify(
            conn,
            "alice",
            User(name="alice", role="admin", disabled=True),
        )
        stored = data.get_one(conn, "alice")

    assert updated.role == "admin"
    assert updated.disabled is True
    assert verify_password("password123", stored.hash)
