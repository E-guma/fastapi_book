import os
import pytest
from model.creature import Creature
from data.error import Missing, Duplicate

# Setup test db in memory
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature
from data.init import init_conn as conn


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    resp = creature.create(conn, sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(conn, sample)


def test_get_one(sample):
    resp = creature.get_one(conn, sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one(conn, "boxturtle")


def test_modify(sample):
    sample.area = "Sesame Street"
    resp = creature.modify(conn, sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Creature = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing):
        _ = creature.modify(conn, thing.name, thing)


def test_modify_duplicate(sample):
    thing: Creature = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    creature.create(thing)
    with pytest.raises(Duplicate):
        _ = creature.modify(conn, sample.name, thing)


def test_delete(sample):
    resp = creature.delete(conn, sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(conn, sample.name)
