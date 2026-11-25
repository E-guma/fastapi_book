from model.explorer import Explorer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import ExplorerORM


def get_one(session: Session, name: str) -> Explorer:
    """Retrieve an explorer by name."""
    orm_explorer = session.get(ExplorerORM, name)
    if orm_explorer is None:
        raise Missing(f"Explorer {name} not found")
    return orm_explorer.to_pydantic()


def get_all(session: Session) -> list[Explorer]:
    """Retrieve all explorers."""
    return [row.to_pydantic() for row in session.query(ExplorerORM).all()]


def create(session: Session, explorer: Explorer) -> Explorer:
    """Create an explorer."""
    db_explorer = ExplorerORM.from_pydantic(explorer)
    try:
        session.add(db_explorer)
        session.flush()
        session.refresh(db_explorer)
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return db_explorer.to_pydantic()


def modify(session: Session, name: str, explorer: Explorer) -> Explorer:
    """Update an explorer."""
    db_explorer = session.get(ExplorerORM, name)
    if db_explorer is None:
        raise Missing(f"Explorer {name} not found")
    try:
        db_explorer.name = explorer.name
        db_explorer.country = explorer.country
        db_explorer.description = explorer.description
        session.flush()
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return db_explorer.to_pydantic()


def delete(session: Session, name: str) -> None:
    """Delete an explorer."""
    db_explorer = session.get(ExplorerORM, name)
    if db_explorer is None:
        raise Missing(f"Explorer {name} not found")
    session.delete(db_explorer)
    session.flush()
