import data.creature as data
from model.creature import Creature
from sqlalchemy.orm import Session


def get_all(conn: Session) -> list[Creature]:
    return data.get_all(conn)


def get_one(conn: Session, name: str) -> Creature:
    return data.get_one(conn, name)


def create(conn: Session, creature: Creature) -> Creature:
    return data.create(conn, creature)


def modify(conn: Session, name: str, creature: Creature) -> Creature:
    return data.modify(conn, name, creature)


def delete(conn: Session, name: str) -> None:
    return data.delete(conn, name)
