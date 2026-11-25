from sqlalchemy.orm import Session

import data.user as data
from model.user import User, UserCreate, UserInDB
from service.auth import get_hash


def _to_user(user: UserInDB) -> User:
    """Remove storage-only fields before returning a user to clients."""
    return User(**user.model_dump(exclude={"hash", "google_sub"}))


def get_all(session: Session) -> list[User]:
    return [_to_user(user) for user in data.get_all(session)]


def get_one(session: Session, name: str) -> User:
    return _to_user(data.get_one(session, name))


def create(
    session: Session,
    user: UserCreate,
    *,
    role: str = "user",
    disabled: bool = False,
) -> User:
    db_user = UserInDB(
        name=user.name,
        role=role,
        disabled=disabled,
        hash=get_hash(user.password),
    )
    return _to_user(data.create(session, db_user))


def modify(session: Session, name: str, user: User) -> User:
    existing = data.get_one(session, name)
    updated = UserInDB(
        name=user.name,
        role=user.role,
        disabled=user.disabled,
        hash=existing.hash,
        google_sub=existing.google_sub,
        email=existing.email,
        email_verified=existing.email_verified,
        picture=existing.picture,
    )
    return _to_user(data.modify(session, name, updated))


def delete(session: Session, name: str) -> None:
    data.delete(session, name)


def delete_all(session: Session) -> None:
    data.delete_all(session)
