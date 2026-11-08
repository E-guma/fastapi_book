import pytest

from model.creature import Creature
from data.error import Missing, Duplicate
from data import creature
from data.init import get_conn_cm


@pytest.fixture
def sample() -> Creature:
    """Return a sample Creature object."""
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


@pytest.fixture
def seeded_creature(sample) -> Creature:
    """Seed a creature into the database for dependent tests."""
    with get_conn_cm() as conn:
        creature.create(conn, sample)
    return sample


def test_create(sample):
    with get_conn_cm() as conn:
        resp = creature.create(conn, sample)
        assert resp == sample


def test_create_duplicate(seeded_creature):
    with pytest.raises(Duplicate), get_conn_cm() as conn:
        creature.create(conn, seeded_creature)


def test_get_all_empty():
    with get_conn_cm() as conn:
        assert creature.get_all(conn) == []


def test_get_all(seeded_creature):
    with get_conn_cm() as conn:
        assert creature.get_all(conn) == [seeded_creature]


def test_get_one(seeded_creature):
    with get_conn_cm() as conn:
        resp = creature.get_one(conn, seeded_creature.name)
        assert resp == seeded_creature


def test_get_one_missing():
    with pytest.raises(Missing), get_conn_cm() as conn:
        creature.get_one(conn, "boxturtle")


def test_modify(seeded_creature):
    with get_conn_cm() as conn:
        seeded_creature.area = "Sesame Street"
        resp = creature.modify(conn, seeded_creature.name, seeded_creature)
        assert resp == seeded_creature


def test_modify_rename(seeded_creature):
    renamed = seeded_creature.model_copy(update={"name": "yeti2"})
    with get_conn_cm() as conn:
        resp = creature.modify(conn, seeded_creature.name, renamed)
        assert resp == renamed
        with pytest.raises(Missing):
            creature.get_one(conn, seeded_creature.name)


def test_modify_missing():
    thing = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing), get_conn_cm() as conn:
        creature.modify(conn, thing.name, thing)


def test_modify_duplicate(seeded_creature):
    thing = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with get_conn_cm() as conn:
        creature.create(conn, thing)
    new_thing = thing.model_copy(update={"country": "US"})
    with pytest.raises(Duplicate), get_conn_cm() as conn:
        creature.modify(conn, seeded_creature.name, new_thing)


def test_delete(seeded_creature):
    with get_conn_cm() as conn:
        assert creature.delete(conn, seeded_creature.name) is None
        with pytest.raises(Missing):
            creature.get_one(conn, seeded_creature.name)


def test_delete_missing():
    with pytest.raises(Missing), get_conn_cm() as conn:
        creature.delete(conn, "nothing")
