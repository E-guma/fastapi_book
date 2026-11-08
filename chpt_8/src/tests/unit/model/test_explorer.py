import pytest
from pydantic import ValidationError

from model.explorer import Explorer


def make_explorer(**overrides) -> Explorer:
    values = {
        "name": "sparrow",
        "country": "NZ",
        "description": "bird person",
    }
    values.update(overrides)
    return Explorer(**values)


def test_strings_are_stripped():
    explorer = make_explorer(name="  sparrow  ", country=" NZ ")
    assert explorer.name == "sparrow"
    assert explorer.country == "NZ"


def test_blank_name_rejected():
    with pytest.raises(ValidationError):
        make_explorer(name="   ")


def test_required_fields():
    with pytest.raises(ValidationError):
        Explorer(name="sparrow")
