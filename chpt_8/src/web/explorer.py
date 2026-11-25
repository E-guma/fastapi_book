import service.explorer as service
from data.error import Duplicate, Missing
from fastapi import APIRouter, Depends, HTTPException
from model.explorer import Explorer

from web.auth import SessionDep, get_current_active_user, require_role

logged_in = [Depends(get_current_active_user)]
admin_only = [Depends(require_role('admin'))]

router = APIRouter(prefix="/explorer", tags=["explorers"])


@router.get("", include_in_schema=False)
@router.get("/", summary="List explorers")
def get_all(session: SessionDep) -> list[Explorer]:
    """Return every explorer in the database."""
    return service.get_all(session)


@router.get(
    "/{name}",
    summary="Get an explorer",
    responses={404: {"description": "Explorer not found"}},
)
def get_one(name: str, session: SessionDep) -> Explorer:
    """Return the explorer with the given name."""
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
    summary="Create an explorer",
    responses={409: {"description": "Explorer already exists"}},
    dependencies=logged_in,
)
def create(explorer: Explorer, session: SessionDep) -> Explorer:
    """Add a new explorer."""
    try:
        return service.create(session, explorer)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch(
    "/{name}",
    summary="Update an explorer",
    responses={
        404: {"description": "Explorer not found"},
        409: {"description": "Explorer name already exists"},
    },
    dependencies=logged_in,
)
def modify(name: str, explorer: Explorer, session: SessionDep) -> Explorer:
    """Update an existing explorer."""
    try:
        return service.modify(session, name, explorer)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete(
    "/{name}",
    status_code=204,
    summary="Delete an explorer",
    responses={404: {"description": "Explorer not found"}},
    dependencies=admin_only,
)
def delete(name: str, session: SessionDep) -> None:
    """Delete the explorer with the given name."""
    try:
        service.delete(session, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
