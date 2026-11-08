import data.creature as data
from model.creature import Creature


def get_all(conn: data.Connection) -> list[Creature]:
    return data.get_all(conn)


def get_one(conn: data.Connection, name: str) -> Creature:
    return data.get_one(conn, name)


def create(conn: data.Connection, creature: Creature) -> Creature:
    return data.create(conn, creature)


# def replace(id, creature: Creature) -> Creature:
#   return data.replace(id, creature)


def modify(conn: data.Connection, name: str, creature: Creature) -> Creature:
    return data.modify(conn, name, creature)


def delete(conn: data.Connection, name: str) -> None:
    return data.delete(conn, name)
