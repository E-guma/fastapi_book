import data.explorer as data
from model.explorer import Explorer
from sqlalchemy.orm import Session


def get_all(session: Session) -> list[Explorer]:
    return data.get_all(session)


def get_one(session: Session, name: str) -> Explorer:
    return data.get_one(session, name)


def create(session: Session, explorer: Explorer) -> Explorer:
    return data.create(session, explorer)


def modify(session: Session, name: str, explorer: Explorer) -> Explorer:
    return data.modify(session, name, explorer)


def delete(session: Session, name: str) -> None:
    return data.delete(session, name)
