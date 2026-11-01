from typing import Annotated
import service.explorer as service
from data.error import Duplicate, Missing
from data.init import get_conn, Connection
from fastapi import APIRouter, HTTPException, Depends
from model.explorer import Explorer

Db = Annotated[Connection, Depends(get_conn)]
router = APIRouter(prefix="/explorer")


@router.get("", include_in_schema=False)
@router.get("/")
def get_all(conn: Db) -> list[Explorer]:
    return service.get_all(conn)


@router.get("/{name}")
def get_one(name: str, conn: Db) -> Explorer:
    try:
        return service.get_one(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
def create(explorer: Explorer, conn: Db) -> Explorer:
    try:
        return service.create(conn, explorer)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch("/{name}")
def modify(name: str, explorer: Explorer, conn: Db) -> Explorer:
    try:
        return service.modify(conn, name, explorer)
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
