import pytest
from pydantic import ValidationError

from model.creature import Creature


def make_creature(**overrides) -> Creature:
    values = {
        "name": "yeti",
        "country": "CN",
        "area": "Himalayas",
        "description": "Hirsute Himalayan",
        "aka": "Abominable Snowman",
    }
    values.update(overrides)
    return Creature(**values)


def test_strings_are_stripped():
    creature = make_creature(name="  yeti  ", country=" CN ")
    assert creature.name == "yeti"
    assert creature.country == "CN"


def test_blank_name_rejected():
    with pytest.raises(ValidationError):
        make_creature(name="   ")


def test_required_fields():
    with pytest.raises(ValidationError):
        Creature(name="yeti")
