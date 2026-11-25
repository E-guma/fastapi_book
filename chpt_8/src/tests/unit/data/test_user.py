import pytest
from data import user
from data.db import get_db_cm
from data.error import Duplicate, Missing
from model.user import UserInDB


@pytest.fixture
def sample() -> UserInDB:
    """Return a sample UserInDB object."""
    return UserInDB(
        name="alice",
        role="user",
        disabled=False,
        hash="not-a-real-hash",
    )


@pytest.fixture
def seeded_user(sample) -> UserInDB:
    """Seed a user into the database for dependent tests."""
    with get_db_cm() as conn:
        user.create(conn, sample)
    return sample


def test_create(sample):
    with get_db_cm() as conn:
        resp = user.create(conn, sample)
        assert resp == sample


def test_create_duplicate(seeded_user):
    with pytest.raises(Duplicate), get_db_cm() as conn:
        user.create(conn, seeded_user)


def test_get_all_empty():
    with get_db_cm() as conn:
        assert user.get_all(conn) == []


def test_get_all(seeded_user):
    with get_db_cm() as conn:
        assert user.get_all(conn) == [seeded_user]


def test_get_one(seeded_user):
    with get_db_cm() as conn:
        resp = user.get_one(conn, seeded_user.name)
        assert resp == seeded_user


def test_get_one_missing():
    with pytest.raises(Missing), get_db_cm() as conn:
        user.get_one(conn, "no one here")


def test_role_and_disabled_round_trip(sample):
    sample.role = "admin"
    sample.disabled = True
    with get_db_cm() as conn:
        resp = user.create(conn, sample)
        assert resp.role == "admin"
        assert resp.disabled is True


def test_modify(seeded_user):
    with get_db_cm() as conn:
        seeded_user.role = "admin"
        seeded_user.disabled = True
        resp = user.modify(conn, seeded_user.name, seeded_user)
        assert resp == seeded_user


def test_modify_rename(seeded_user):
    renamed = seeded_user.model_copy(update={"name": "alice2"})
    with get_db_cm() as conn:
        resp = user.modify(conn, seeded_user.name, renamed)
        assert resp == renamed
        with pytest.raises(Missing):
            user.get_one(conn, seeded_user.name)


def test_modify_missing():
    thing = UserInDB(name="nobody", hash="not-a-real-hash")
    with pytest.raises(Missing), get_db_cm() as conn:
        user.modify(conn, thing.name, thing)


def test_modify_duplicate(seeded_user):
    thing = UserInDB(name="bob", hash="not-a-real-hash")
    with get_db_cm() as conn:
        user.create(conn, thing)
    thing.role = "admin"
    with pytest.raises(Duplicate), get_db_cm() as conn:
        user.modify(conn, seeded_user.name, thing)


def test_delete(seeded_user):
    with get_db_cm() as conn:
        assert user.delete(conn, seeded_user.name) is None
        with pytest.raises(Missing):
            user.get_one(conn, seeded_user.name)


def test_delete_missing():
    with pytest.raises(Missing), get_db_cm() as conn:
        user.delete(conn, "nothing")
