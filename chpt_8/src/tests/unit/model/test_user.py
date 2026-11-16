import pytest
from model.user import User, UserCreate, UserInDB
from pydantic import ValidationError


def test_user_defaults():
    user = User(name="alice")

    assert user.role == "user"
    assert user.disabled is False
    assert not hasattr(user, "hash")
    assert not hasattr(user, "password")


def test_user_rejects_unknown_role():
    with pytest.raises(ValidationError):
        User(name="alice", role="root")


def test_user_name_bounds():
    with pytest.raises(ValidationError):
        User(name="")
    with pytest.raises(ValidationError):
        User(name="x" * 65)
    assert User(name="x" * 64).name == "x" * 64


def test_user_strips_whitespace():
    assert User(name="  alice  ").name == "alice"


def test_user_create_password_bounds():
    with pytest.raises(ValidationError):
        UserCreate(name="alice", password="short")
    with pytest.raises(ValidationError):
        UserCreate(name="alice", password="x" * 129)
    assert UserCreate(name="alice", password="x" * 128).password == "x" * 128


def test_user_create_inherits_defaults():
    user = UserCreate(name="alice", password="password123")

    assert user.role == "user"
    assert user.disabled is False


def test_user_in_db_requires_hash():
    with pytest.raises(ValidationError):
        UserInDB(name="alice")

    user = UserInDB(name="alice", hash="hashed-password")

    assert user.hash == "hashed-password"
    assert user.role == "user"
    assert user.disabled is False
