from uuid import UUID

from model.user import UserInDB
from sqlalchemy import delete as sql_delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.error import Duplicate, Missing
from data.models import UserORM


def get_all(session: Session) -> list[UserInDB]:
    """Retrieve all users."""
    return [row.to_pydantic() for row in session.query(UserORM).all()]


def get_one(session: Session, id: UUID) -> UserInDB:
    """Retrieve one user by primary key."""
    orm_user = session.get(UserORM, id)
    if orm_user is None:
        raise Missing(f"User {id} not found")
    return orm_user.to_pydantic()


def get_by_username(session: Session, name: str) -> UserInDB | None:
    """Find a password user by username; Google accounts never match."""
    orm_user = (
        session.query(UserORM)
        .filter_by(name=name, google_sub=None)
        .one_or_none()
    )
    return orm_user.to_pydantic() if orm_user else None


def get_by_google_sub(session: Session, google_sub: str) -> UserInDB | None:
    """Find a user by their stable Google subject id."""
    orm_user = (
        session.query(UserORM).filter_by(google_sub=google_sub).one_or_none()
    )
    return orm_user.to_pydantic() if orm_user else None


def create(session: Session, user: UserInDB) -> UserInDB:
    """Create a user."""
    db_user = UserORM.from_pydantic(user)
    try:
        session.add(db_user)
        session.flush()
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    return db_user.to_pydantic()


def modify(session: Session, id: UUID, user: UserInDB) -> UserInDB:
    """Modify a user."""
    db_user = session.get(UserORM, id)
    if db_user is None:
        raise Missing(f"User {id} not found")
    try:
        db_user.name = user.name
        db_user.hash = user.hash
        db_user.role = user.role
        db_user.disabled = user.disabled
        db_user.google_sub = user.google_sub
        db_user.email = user.email
        db_user.email_verified = user.email_verified
        db_user.picture = user.picture
        session.flush()
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    return db_user.to_pydantic()


def delete(session: Session, id: UUID) -> None:
    """Delete a user."""
    db_user = session.get(UserORM, id)
    if db_user is None:
        raise Missing(f"User {id} not found")
    session.delete(db_user)
    session.flush()


def delete_all(session: Session) -> None:
    """Use with Catioun! Deletes all Users"""
    session.execute(sql_delete(UserORM).where(UserORM.role=='user'))
