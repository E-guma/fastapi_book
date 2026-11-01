import os
import pytest
from model.explorer import Explorer
from data.error import Missing, Duplicate

# Setup test db in memory
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer
from data.init import init_conn as conn


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="sparrow",
        country="NZ",
        description="bird person",
    )


def test_create(sample):
    resp = explorer.create(conn, sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(conn, sample)


def test_get_one(sample):
    resp = explorer.get_one(conn, sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = explorer.get_one(conn, "boxturtle")


def test_modify(sample):
    sample.area = "Sesame Street"
    resp = explorer.modify(conn, sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Explorer = Explorer(name="snurfle", country="RU", description="some thing")
    with pytest.raises(Missing):
        _ = explorer.modify(conn, thing.name, thing)


def test_modify_duplicate(sample):
    thing: Explorer = Explorer(name="snurfle", country="RU", description="some thing")
    explorer.create(thing)
    with pytest.raises(Duplicate):
        _ = explorer.modify(conn, sample.name, thing)


def test_delete(sample):
    resp = explorer.delete(conn, sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(conn, sample.name)
