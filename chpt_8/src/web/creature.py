import service.creature as service
from data.error import Duplicate, Missing
from fastapi import APIRouter, Depends, HTTPException
from model.creature import Creature

from web.auth import SessionDep, get_current_active_user, require_role

logged_in = [Depends(get_current_active_user)]
admin_only = [Depends(require_role('admin'))]

router = APIRouter(prefix="/creature", tags=["creatures"])


@router.get("", include_in_schema=False)
@router.get("/", summary="List creatures")
def get_all(session: SessionDep) -> list[Creature]:
    """Return every creature in the database."""
    return service.get_all(session)


@router.get(
    "/{name}",
    summary="Get a creature",
    responses={404: {"description": "Creature not found"}},
)
def get_one(name: str, session: SessionDep) -> Creature:
    """Return the creature with the given name."""
    try:
        return service.get_one(session, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post(
    "", status_code=201, include_in_schema=False, dependencies=logged_in
)
@router.post(
    "/",
    status_code=201,
    summary="Create a creature",
    responses={409: {"description": "Creature already exists"}},
    dependencies=logged_in,
)
def create(creature: Creature, session: SessionDep) -> Creature:
    """Add a new creature."""
    try:
        return service.create(session, creature)
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
def modify(name: str, creature: Creature, session: SessionDep) -> Creature:
    """Update an existing creature."""
    try:
        return service.modify(session, name, creature)
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
def delete(name: str, session: SessionDep) -> None:
    """Delete the creature with the given name."""
    try:
        service.delete(session, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
