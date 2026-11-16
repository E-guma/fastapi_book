from typing import Annotated
import service.creature as service
from data.error import Duplicate, Missing
from fastapi import APIRouter, HTTPException, Depends
from model.creature import Creature

from web.auth import Db, get_current_active_user, require_role

logged_in = [Depends(get_current_active_user)]
admin_only = [Depends(require_role('admin'))]

router = APIRouter(prefix="/creature", tags=["creatures"])


@router.get("", include_in_schema=False)
@router.get("/", summary="List creatures")
def get_all(conn: Db) -> list[Creature]:
    """Return every creature in the database."""
    return service.get_all(conn)


@router.get(
    "/{name}",
    summary="Get a creature",
    responses={404: {"description": "Creature not found"}},
)
def get_one(name: str, conn: Db) -> Creature:
    """Return the creature with the given name."""
    try:
        return service.get_one(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False,
             dependencies=logged_in)
@router.post(
    "/",
    status_code=201,
    summary="Create a creature",
    responses={409: {"description": "Creature already exists"}},
    dependencies=logged_in,
)
def create(creature: Creature, conn: Db) -> Creature:
    """Add a new creature."""
    try:
        return service.create(conn, creature)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch(
    "/{name}",
    summary="Update a creature",
    responses={
        404: {"description": "Creature not found"},
        409: {"description": "Creature name already exists"},
    },
    dependencies=logged_in,
)
def modify(name: str, creature: Creature, conn: Db) -> Creature:
    """Update an existing creature."""
    try:
        return service.modify(conn, name, creature)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete(
    "/{name}",
    status_code=204,
    summary="Delete a creature",
    responses={404: {"description": "Creature not found"}},
    dependencies=admin_only,
)
def delete(name: str, conn: Db):
    """Delete the creature with the given name."""
    try:
        service.delete(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
