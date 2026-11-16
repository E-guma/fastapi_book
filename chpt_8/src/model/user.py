from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Public user profile returned by the API."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=64)
    role: Literal["user", "admin"] = "user"
    disabled: bool = False


class UserCreate(User):
    """Registration payload containing the plain-text password."""

    password: str = Field(min_length=8, max_length=128)


class UserInDB(User):
    """User record persisted to the database, including the password hash."""

    hash: str
