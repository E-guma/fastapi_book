from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import UserORM


def get_all(db: Session) -> list:
    """Retrieve all users."""
    return [row.to_pydantic() for row in db.query(UserORM).all()]


def get_one(db: Session, name: str):
    """Retrieve one user."""
    orm_user = db.get(UserORM, name)
    if orm_user is None:
        raise Missing(f"User {name} not found")
    return orm_user.to_pydantic()


def create(db: Session, user):
    """Create a user."""
    db_user = UserORM.from_pydantic(user)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise Duplicate(f"User {user.name} already exists")
    return db_user.to_pydantic()


def modify(db: Session, name: str, user):
    """Modify a user."""
    db_user = db.get(UserORM, name)
    if db_user is None:
        raise Missing(f"User {name} not found")
    try:
        db_user.name = user.name
        db_user.hash = user.hash
        db_user.role = user.role
        db_user.disabled = user.disabled
        db.commit()
    except IntegrityError:
        db.rollback()
        raise Duplicate(f"User {user.name} already exists")
    return db_user.to_pydantic()


def delete(db: Session, name: str) -> None:
    """Delete a user."""
    db_user = db.get(UserORM, name)
    if db_user is None:
        raise Missing(f"User {name} not found")
    db.delete(db_user)
    db.commit()
    return None
