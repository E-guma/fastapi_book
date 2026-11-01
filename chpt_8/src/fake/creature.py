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
    """Return all creatures"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Return named Creature"""
    for creature in _creatures:
        if creature.name == name:
            return creature
    return None


def create(creature: Creature) -> Creature:
    """Add a Creature"""
    return creature


def modify(id, creature: Creature) -> Creature:
    """Partially modify a Creature"""
    return creature


def replace(id, creature: Creature) -> Creature:
    """Replace a creature"""
    return creature


def delete(id, name: str) -> bool:
    """Delete a creature; return None if it existed"""
    return None
