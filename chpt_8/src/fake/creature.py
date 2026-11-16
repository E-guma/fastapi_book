from model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch",
    ),
]


def get_all() -> list[Creature]:
    """Return all creatures."""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Return the creature with the given name, if present."""
    for creature in _creatures:
        if creature.name == name:
            return creature
    return None


def create(creature: Creature) -> Creature:
    """Return the supplied creature without persisting it."""
    return creature


def modify(id, creature: Creature) -> Creature:
    """Return the supplied creature without applying changes."""
    return creature


def replace(id, creature: Creature) -> Creature:
    """Return the supplied creature without replacing stored state."""
    return creature


def delete(id, name: str) -> bool:
    """Return None; deletions are no-ops in the fake store."""
    return None
