from fastapi import APIRouter, Depends, HTTPException

import service.user as service
from data.error import Duplicate, Missing
from model.user import User, UserCreate
from web.auth import SessionDep, require_role

router = APIRouter(
    prefix="/user", tags=["user"], dependencies=[Depends(require_role("admin"))]
)


@router.get("", include_in_schema=False)
@router.get("/")
def get_all(session: SessionDep) -> list[User]:
    return service.get_all(session)


@router.get("/{name}")
def get_one(name: str, session: SessionDep) -> User:
    try:
        return service.get_one(session, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
def create(user: UserCreate, session: SessionDep) -> User:
    try:
        return service.create(session, user, role="user", disabled=False)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch("/{name}", status_code=200)
def modify(name: str, user: User, session: SessionDep) -> User:
    try:
        return service.modify(session, name, user)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.delete("/delete_all", status_code=204)
def delete_all(session: SessionDep) -> None:
    service.delete_all(session)


@router.delete("/{name}", status_code=204)
def delete(name: str, session: SessionDep) -> None:
    try:
        service.delete(session, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
