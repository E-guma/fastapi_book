from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import ExplorerORM


def get_one(db: Session, name: str):
    """Retrieve an explorer by name."""
    orm_explorer = db.get(ExplorerORM, name)
    if orm_explorer is None:
        raise Missing(f"Explorer {name} not found")
    return orm_explorer.to_pydantic()


def get_all(db: Session) -> list:
    """Retrieve all explorers."""
    return [row.to_pydantic() for row in db.query(ExplorerORM).all()]


def create(db: Session, explorer):
    """Create an explorer."""
    db_explorer = ExplorerORM.from_pydantic(explorer)
    try:
        db.add(db_explorer)
        db.commit()
        db.refresh(db_explorer)
    except IntegrityError:
        db.rollback()
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return db_explorer.to_pydantic()


def modify(db: Session, name: str, explorer):
    """Update an explorer."""
    db_explorer = db.get(ExplorerORM, name)
    if db_explorer is None:
        raise Missing(f"Explorer {name} not found")
    try:
        db_explorer.name = explorer.name
        db_explorer.country = explorer.country
        db_explorer.description = explorer.description
        db.commit()
    except IntegrityError:
        db.rollback()
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return db_explorer.to_pydantic()


def delete(db: Session, name: str):
    """Delete an explorer."""
    db_explorer = db.get(ExplorerORM, name)
    if db_explorer is None:
        raise Missing(f"Explorer {name} not found")
    db.delete(db_explorer)
    db.commit()
    return None
