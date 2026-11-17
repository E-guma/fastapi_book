import data.explorer as data
from model.explorer import Explorer
from sqlalchemy.orm import Session


def get_all(conn: Session) -> list[Explorer]:
    return data.get_all(conn)


def get_one(conn: Session, name: str) -> Explorer:
    return data.get_one(conn, name)


def create(conn: Session, explorer: Explorer) -> Explorer:
    return data.create(conn, explorer)


def modify(conn: Session, name: str, explorer: Explorer) -> Explorer:
    return data.modify(conn, name, explorer)


def delete(conn: Session, name: str) -> None:
    return data.delete(conn, name)
