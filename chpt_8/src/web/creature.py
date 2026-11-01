from typing import Annotated
import service.creature as service
from data.error import Duplicate, Missing
from data.init import get_conn, Connection
from fastapi import APIRouter, HTTPException, Depends
from model.creature import Creature

Db = Annotated[Connection, Depends(get_conn)]
router = APIRouter(prefix="/creature")


@router.get("", include_in_schema=False)
@router.get("/")
def get_all(conn: Db) -> list[Creature]:
    return service.get_all(conn)


@router.get("/{name}")
def get_one(name: str, conn: Db) -> Creature | None:
    try:
        return service.get_one(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
def create(creature: Creature, conn: Db) -> Creature:
    try:
        return service.create(conn, creature)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch("/{name}")
def modify(name: str, creature: Creature, conn: Db) -> Creature:
    try:
        return service.modify(conn, name, creature)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete("/{name}", status_code=204)
def delete(name: str, conn: Db):
    try:
        service.delete(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
