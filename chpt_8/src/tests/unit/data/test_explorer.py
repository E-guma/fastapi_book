import os
import pytest

from model.explorer import Explorer
from data.error import Missing, Duplicate
from data import explorer
from data.init import get_conn_cm


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="sparrow",
        country="NZ",
        description="bird person",
    )


@pytest.fixture
def seeded_explorer(sample) -> Explorer:
    with get_conn_cm() as conn:
        explorer.create(conn, sample)
    return sample


def test_create(sample):
    with get_conn_cm() as conn:
        resp = explorer.create(conn, sample)
        assert resp == sample


def test_create_duplicate(seeded_explorer):
    with pytest.raises(Duplicate):
        with get_conn_cm() as conn:
            explorer.create(conn, seeded_explorer)


def test_get_one(seeded_explorer):
    with get_conn_cm() as conn:
        resp = explorer.get_one(conn, seeded_explorer.name)
        assert resp == seeded_explorer


def test_get_one_missing():
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            explorer.get_one(conn, "no one here")


def test_modify(seeded_explorer):
    with get_conn_cm() as conn:
        seeded_explorer.country = "SW"
        resp = explorer.modify(conn, seeded_explorer.name, seeded_explorer)
        assert resp == seeded_explorer


def test_modify_missing():
    thing = Explorer(name="snurfle", country="RU", description="some thing")
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            explorer.modify(conn, thing.name, thing)


def test_modify_duplicate(seeded_explorer):
    thing = Explorer(name="snurfle", country="RU", description="some thing")
    with get_conn_cm() as conn:
        explorer.create(conn, thing)
    thing.country = "US"
    with pytest.raises(Duplicate):
        with get_conn_cm() as conn:
            explorer.modify(conn, seeded_explorer.name, thing)


def test_delete(seeded_explorer):
    with get_conn_cm() as conn:
        resp = explorer.delete(conn, seeded_explorer.name)
        assert resp is None


def test_delete_missing():
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            explorer.delete(conn, "nothing")
