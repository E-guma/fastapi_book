import data.explorer as data
from model.explorer import Explorer


def get_all(conn: data.Connection) -> list[Explorer]:
    return data.get_all(conn)


def get_one(conn: data.Connection, name: str) -> Explorer:
    return data.get_one(conn, name)


def create(conn: data.Connection, explorer: Explorer) -> Explorer:
    return data.create(conn, explorer)


# def replace(id, explorer: Explorer) -> Explorer:
#    return data.replace(id, explorer)


def modify(conn: data.Connection, name: str, explorer: Explorer) -> Explorer:
    return data.modify(conn, name, explorer)


def delete(conn: data.Connection, name: str) -> None:
    return data.delete(conn, name)
