from data.error import Duplicate, Missing
from fastapi import APIRouter, HTTPException, Depends
from model.user import User, UserCreate
from service import user as service

from web.auth import Db, require_role

router = APIRouter(
    prefix="/user", tags=["user"], dependencies=[Depends(require_role("admin"))]
)


@router.get("", include_in_schema=False)
@router.get("/")
def get_all(conn: Db) -> list[User]:
    return service.get_all(conn)


@router.get("/{name}")
def get_one(name: str, conn: Db) -> User:
    try:
        return service.get_one(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
def create(user: UserCreate, conn: Db) -> User:
    try:
        # Public signup: role and disabled are server-controlled.
        return service.create(conn, user, role="user", disabled=False)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.patch("/{name}", status_code=200)
def modify(name: str, user: User, conn: Db) -> User:
    try:
        return service.modify(conn, name, user)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)

@router.delete("/delete_all", status_code=204)
def delete_all(conn: Db) -> None:
    service.delete_all(conn)

@router.delete("/{name}", status_code=204)
def delete(name: str, conn: Db) -> None:
    try:
        service.delete(conn, name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
