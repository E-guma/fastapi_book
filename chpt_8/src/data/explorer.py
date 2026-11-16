from model.explorer import Explorer

from .error import Duplicate, Missing
from .init import IntegrityError, Connection


def row_to_model(row: tuple) -> Explorer:
    """Map a database row to an Explorer."""
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    """Convert an Explorer to a dictionary of column values."""
    return explorer.model_dump()


def get_one(conn: Connection, name: str) -> Explorer:
    """Retrieve an explorer by name."""
    curs = conn.cursor()
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Explorer {name} not found")


def get_all(conn: Connection) -> list[Explorer]:
    """Retrieve all explorers."""
    curs = conn.cursor()
    qry = "select * from explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def modify(conn: Connection, name: str, explorer: Explorer) -> Explorer:
    """Update an explorer."""
    curs = conn.cursor()
    qry = """update explorer set 
            name=:name,
            country=:country,
            description=:description
            where name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists")
    if curs.rowcount == 1:
        return get_one(conn, explorer.name)
    else:
        raise Missing(f"Explorer {name} not found")


def create(conn: Connection, explorer: Explorer) -> Explorer:
    """Create an explorer."""
    curs = conn.cursor()
    qry = "insert into explorer values(:name, :country, :description)"
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return get_one(conn, explorer.name)


def delete(conn: Connection, name: str):
    """Delete an explorer."""
    curs = conn.cursor()
    qry = "delete from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return
    else:
        raise Missing(f"Explorer {name} not found")
