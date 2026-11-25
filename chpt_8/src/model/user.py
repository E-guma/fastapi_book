from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Public user profile returned by the API."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=64)
    role: Literal["user", "admin"] = "user"
    disabled: bool = False
    email: str | None = None
    email_verified: bool = False
    picture: str | None = None


class UserCreate(User):
    """Registration payload containing the plain-text password."""

    password: str = Field(min_length=8, max_length=128)


class UserInDB(User):
    """User record persisted to the database, including the password hash."""

    hash: str
    google_sub: str | None = None

class GoogleUserInfo(BaseModel):
    """Verified claims extracted from Google's ID token."""

    sub: str = Field(min_length=1, max_length=255)
    email: str | None = None
    email_verified: bool = False
    name: str | None = None
    picture: str | None = None
