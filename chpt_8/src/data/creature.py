from model.creature import Creature
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import CreatureORM


def get_one(session: Session, name: str) -> Creature:
    """Retrieve a creature by name."""
    orm_creature = session.get(CreatureORM, name)
    if orm_creature is None:
        raise Missing(f"Creature {name} not found")
    return orm_creature.to_pydantic()


def get_all(session: Session) -> list[Creature]:
    """Retrieve all creatures."""
    return [row.to_pydantic() for row in session.query(CreatureORM).all()]


def create(session: Session, creature: Creature) -> Creature:
    """Create a creature."""
    db_creature = CreatureORM.from_pydantic(creature)
    try:
        session.add(db_creature)
        session.flush()
        session.refresh(db_creature)
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return db_creature.to_pydantic()


def modify(session: Session, name: str, creature: Creature) -> Creature:
    """Update a creature."""
    db_creature = session.get(CreatureORM, name)
    if db_creature is None:
        raise Missing(f"Creature {name} not found")
    try:
        db_creature.name = creature.name
        db_creature.country = creature.country
        db_creature.area = creature.area
        db_creature.description = creature.description
        db_creature.aka = creature.aka
        session.flush()
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return db_creature.to_pydantic()


def delete(session: Session, name: str) -> None:
    """Delete a creature."""
    db_creature = session.get(CreatureORM, name)
    if db_creature is None:
        raise Missing(f"Creature {name} not found")
    session.delete(db_creature)
    session.flush()
