import data.user as data
from model.user import User, UserCreate, UserInDB

from service.auth import get_hash


def _to_user(user: UserInDB) -> User:
    """Remove storage-only fields before returning a user to clients."""
    return User(**user.model_dump(exclude={"hash"}))


def get_all(conn: data.Connection) -> list[User]:
    return [_to_user(user) for user in data.get_all(conn)]


def get_one(conn: data.Connection, name: str) -> User:
    return _to_user(data.get_one(conn, name))


def create(
    conn: data.Connection,
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
    return _to_user(data.create(conn, db_user))


def modify(conn: data.Connection, name: str, user: User) -> User:
    existing = data.get_one(conn, name)
    updated = UserInDB(
        name=user.name,
        role=user.role,
        disabled=user.disabled,
        hash=existing.hash,
    )
    return _to_user(data.modify(conn, name, updated))


def delete(conn: data.Connection, name: str) -> None:
    return data.delete(conn, name)
