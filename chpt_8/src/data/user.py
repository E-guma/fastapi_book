from model.user import User
from .error import Duplicate, Missing
from .init import IntegrityError, Connection


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict[str, str]:
    return user.model_dump()


def get_all(conn: Connection) -> list[User]:
    curs = conn.cursor()
    qry = "select * from user"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def get_one(conn: Connection, name: str) -> User:
    curs = conn.cursor()
    qry = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"User {name} not found")


def create(conn: Connection, user: User):
    curs = conn.cursor()
    qry = "insert into user values(:name, :hash)"
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"User {user.name} already exists")
    return get_one(conn, user.name)


def modify(conn: Connection, name: str, user: User) -> User:
    """Modifies a user"""
    curs = conn.cursor()
    qry = """update user set 
            name=:name,
            hash=:hash,
            where name=:name_orig"""
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


def delete(conn: Connection, name: str):
    """Delete an user"""
    curs = conn.cursor()
    qry = "delete from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return
    else:
        raise Missing(f"User {name} not found")
