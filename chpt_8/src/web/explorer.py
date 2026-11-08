from typing import Annotated
import service.explorer as service
from data.error import Duplicate, Missing
from data.init import get_conn, Connection
from fastapi import APIRouter, HTTPException, Depends
from model.explorer import Explorer

Db = Annotated[Connection, Depends(get_conn)]
router = APIRouter(prefix="/explorer", tags=["explorers"])


@router.get("", include_in_schema=False)
@router.get("/", summary="List explorers")
def get_all(conn: Db) -> list[Explorer]:
    """Return every explorer in the database."""
    return service.get_all(conn)


@router.get(
    "/{name}",
    summary="Get an explorer",
    responses={404: {"description": "Explorer not found"}},
)
def get_one(name: str, conn: Db) -> Explorer:
    """Return the explorer with the given name."""
    try:
        return service.get_one(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False)
@router.post(
    "/",
    status_code=201,
    summary="Create an explorer",
    responses={409: {"description": "Explorer already exists"}},
)
def create(explorer: Explorer, conn: Db) -> Explorer:
    """Add a new explorer."""
    try:
        return service.create(conn, explorer)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch(
    "/{name}",
    summary="Update an explorer",
    responses={
        404: {"description": "Explorer not found"},
        409: {"description": "Explorer name already exists"},
    },
)
def modify(name: str, explorer: Explorer, conn: Db) -> Explorer:
    """Update an existing explorer."""
    try:
        return service.modify(conn, name, explorer)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete(
    "/{name}",
    status_code=204,
    summary="Delete an explorer",
    responses={404: {"description": "Explorer not found"}},
)
def delete(name: str, conn: Db):
    """Delete the explorer with the given name."""
    try:
        service.delete(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
