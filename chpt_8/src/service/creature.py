from sqlalchemy.orm import Session

import data.creature as data
from model.creature import Creature


def get_all(session: Session) -> list[Creature]:
    return data.get_all(session)


def get_one(session: Session, name: str) -> Creature:
    return data.get_one(session, name)


def create(session: Session, creature: Creature) -> Creature:
    return data.create(session, creature)


def modify(session: Session, name: str, creature: Creature) -> Creature:
    return data.modify(session, name, creature)


def delete(session: Session, name: str) -> None:
    return data.delete(session, name)
