from model.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return named explorer"""
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """Add an Explorer"""
    return explorer


def modify(id, explorer: Explorer) -> Explorer:
    """Partially modify an explorer"""
    return explorer


def replace(id, explorer: Explorer) -> Explorer:
    """Replace an explorer"""
    return explorer


def delete(name: str) -> bool:
    """Delete an explorer; return None if it existed"""
    return None
