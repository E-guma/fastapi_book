from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import CreatureORM
from model.creature import Creature


def get_one(db: Session, name: str) -> Creature:
    """Retrieve a creature by name."""
    orm_creature = db.get(CreatureORM, name)
    if orm_creature is None:
        raise Missing(f"Creature {name} not found")
    return orm_creature.to_pydantic()


def get_all(db: Session) -> list[Creature]:
    """Retrieve all creatures."""
    return [row.to_pydantic() for row in db.query(CreatureORM).all()]


def create(db: Session, creature: Creature) -> Creature:
    """Create a creature."""
    db_creature = CreatureORM.from_pydantic(creature)
    try:
        db.add(db_creature)
        db.flush()
        db.refresh(db_creature)
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return db_creature.to_pydantic()


def modify(db: Session, name: str, creature: Creature) -> Creature:
    """Update a creature."""
    db_creature = db.get(CreatureORM, name)
    if db_creature is None:
        raise Missing(f"Creature {name} not found")
    try:
        db_creature.name = creature.name
        db_creature.country = creature.country
        db_creature.area = creature.area
        db_creature.description = creature.description
        db_creature.aka = creature.aka
        db.flush()
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return db_creature.to_pydantic()


def delete(db: Session, name: str):
    """Delete a creature."""
    db_creature = db.get(CreatureORM, name)
    if db_creature is None:
        raise Missing(f"Creature {name} not found")
    db.delete(db_creature)
    db.flush()
    return None
