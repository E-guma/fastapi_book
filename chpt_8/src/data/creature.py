from model.creature import Creature

from .error import Duplicate, Missing
from .init import IntegrityError, Connection


def row_to_model(row: tuple) -> Creature:
    """Resolves db row tuple to Creature object"""
    return Creature(
        name=row[0], country=row[1], area=row[2], description=row[3], aka=row[4]
    )


def model_to_dict(creature: Creature) -> dict:
    """Resolve model object to dict"""
    return creature.model_dump()


def get_one(conn: Connection, name: str) -> Creature:
    """Retrieves one Creature"""
    curs = conn.cursor()
    qry = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Creature {name} not found")


def get_all(conn: Connection) -> list[Creature]:
    """Retrievs all Creatures"""
    curs = conn.cursor()
    qry = "select * from creature"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(conn: Connection, creature: Creature) -> Creature:
    """Create a creature"""
    curs = conn.cursor()
    qry = "insert into creature values(:name, :country, :area, :description, :aka)"
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    return get_one(conn, creature.name)


def modify(conn: Connection, name: str, creature: Creature) -> Creature:
    """Modify a creature"""
    curs = conn.cursor()
    qry = """Update creature 
            set name=:name, 
            country=:country, 
            area=:area, 
            description=:description, 
            aka=:aka 
            where name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = name
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Creature {creature.name} already exists")
    if curs.rowcount == 1:
        return get_one(conn, creature.name)
    else:
        raise Missing(f"Creature {name} not found")


def delete(conn: Connection, name: str):
    """Delete a creature"""
    curs = conn.cursor()
    qry = "delete from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return
    else:
        raise Missing(f"Creature {name} not found")
