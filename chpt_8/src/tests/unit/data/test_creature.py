import os
import pytest

from model.creature import Creature
from data.error import Missing, Duplicate
from data import creature
from data.init import get_conn_cm


@pytest.fixture
def sample() -> Creature:
    """ "Returns a sample Creature Object"""
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


@pytest.fixture
def seeded_creature(sample) -> Creature:
    """Seeds a creature instance into database for dependent tests"""
    with get_conn_cm() as conn:
        creature.create(conn, sample)
    return sample


def test_create(sample):
    with get_conn_cm() as conn:
        resp = creature.create(conn, sample)
        assert resp == sample


def test_create_duplicate(seeded_creature):
    with pytest.raises(Duplicate):
        with get_conn_cm() as conn:
            creature.create(conn, seeded_creature)


def test_get_one(seeded_creature):
    with get_conn_cm() as conn:
        resp = creature.get_one(conn, seeded_creature.name)
        assert resp == seeded_creature


def test_get_one_missing():
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            creature.get_one(conn, "boxturtle")


def test_modify(seeded_creature):
    with get_conn_cm() as conn:
        seeded_creature.area = "Sesame Street"
        resp = creature.modify(conn, seeded_creature.name, seeded_creature)
        assert resp == seeded_creature


def test_modify_missing():
    thing = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            creature.modify(conn, thing.name, thing)


def test_modify_duplicate(seeded_creature):
    thing = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with get_conn_cm() as conn:
        creature.create(conn, thing)
    new_thing = thing.model_copy(update={"country": "US"})
    with pytest.raises(Duplicate):
        with get_conn_cm() as conn:
            creature.modify(conn, seeded_creature.name, new_thing)


def test_delete(seeded_creature):
    with get_conn_cm() as conn:
        resp = creature.delete(conn, seeded_creature.name)
        assert resp is None


def test_delete_missing():
    with pytest.raises(Missing):
        with get_conn_cm() as conn:
            creature.delete(conn, "nothing")
