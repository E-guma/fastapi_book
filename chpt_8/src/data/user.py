from model.user import UserInDB

from .error import Duplicate, Missing
from .init import Connection, IntegrityError

USER_COLUMNS = "name, hash, role, disabled"


def row_to_model(row: tuple) -> UserInDB:
    """Resolve a database row to a UserInDB object."""
    name, hash, role, disabled = row
    return UserInDB(
        name=name,
        hash=hash,
        role=role,
        disabled=bool(disabled),
    )


def model_to_dict(user: UserInDB) -> dict[str, object]:
    """Resolve a UserInDB object to a dictionary of column values."""
    return user.model_dump()


def get_all(conn: Connection) -> list[UserInDB]:
    """Retrieve all users."""
    curs = conn.cursor()
    qry = f"select {USER_COLUMNS} from user"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def get_one(conn: Connection, name: str) -> UserInDB:
    """Retrieve one user."""
    curs = conn.cursor()
    qry = f"select {USER_COLUMNS} from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"User {name} not found")


def create(conn: Connection, user: UserInDB) -> UserInDB:
    """Create a user."""
    curs = conn.cursor()
    qry = """
        insert into user(name, hash, role, disabled)
        values(:name, :hash, :role, :disabled)
    """
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    return get_one(conn, user.name)


def modify(conn: Connection, name: str, user: UserInDB) -> UserInDB:
    """Modify a user."""
    curs = conn.cursor()
    qry = """
        update user set
            name=:name,
            hash=:hash,
            role=:role,
            disabled=:disabled
        where name=:name_orig
    """
    params = model_to_dict(user)
    params["name_orig"] = name
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    if curs.rowcount == 1:
        return get_one(conn, user.name)
    else:
        raise Missing(f"User {name} not found")


def delete(conn: Connection, name: str) -> None:
    """Delete a user."""
    curs = conn.cursor()
    qry = "delete from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return
    else:
        raise Missing(f"User {name} not found")
