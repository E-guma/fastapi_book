from model.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    """Return all explorers."""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return the explorer with the given name, if present."""
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """Return the supplied explorer without persisting it."""
    return explorer


def modify(id, explorer: Explorer) -> Explorer:
    """Return the supplied explorer without applying changes."""
    return explorer


def replace(id, explorer: Explorer) -> Explorer:
    """Return the supplied explorer without replacing stored state."""
    return explorer


def delete(name: str) -> bool:
    """Return None; deletions are no-ops in the fake store."""
    return None
