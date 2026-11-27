"""SQLAlchemy ORM models."""

from uuid import UUID, uuid4

from model.creature import Creature
from model.explorer import Explorer
from model.user import UserInDB
from sqlalchemy import Index, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class CreatureORM(Base):
    __tablename__ = "creature"

    name: Mapped[str] = mapped_column(primary_key=True)
    country: Mapped[str]
    area: Mapped[str]
    description: Mapped[str]
    aka: Mapped[str]

    def to_pydantic(self) -> Creature:
        return Creature(
            name=self.name,
            country=self.country,
            area=self.area,
            description=self.description,
            aka=self.aka,
        )

    @classmethod
    def from_pydantic(cls, creature: Creature) -> "CreatureORM":
        return cls(
            name=creature.name,
            country=creature.country,
            area=creature.area,
            description=creature.description,
            aka=creature.aka,
        )


class ExplorerORM(Base):
    __tablename__ = "explorer"

    name: Mapped[str] = mapped_column(primary_key=True)
    country: Mapped[str]
    description: Mapped[str]

    def to_pydantic(self) -> Explorer:
        return Explorer(
            name=self.name,
            country=self.country,
            description=self.description,
        )

    @classmethod
    def from_pydantic(cls, explorer: Explorer) -> "ExplorerORM":
        return cls(
            name=explorer.name,
            country=explorer.country,
            description=explorer.description,
        )


class UserORM(Base):
    __tablename__ = "user"
    __table_args__ = (
        # Usernames must be unique for password login, but Google users are
        # free to share a display name (they are identified by google_sub).
        Index(
            "ix_user_username",
            "name",
            unique=True,
            sqlite_where=text("google_sub IS NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(index=True)
    hash: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
    disabled: Mapped[bool] = mapped_column(default=False)
    google_sub: Mapped[str | None] = mapped_column(unique=True, index=True)
    email: Mapped[str | None]
    email_verified: Mapped[bool] = mapped_column(default=False)
    picture: Mapped[str | None]

    def to_pydantic(self) -> UserInDB:
        return UserInDB(
            id=self.id,
            name=self.name,
            hash=self.hash,
            role=self.role,
            disabled=self.disabled,
            google_sub=self.google_sub,
            email=self.email,
            email_verified=self.email_verified,
            picture=self.picture,
        )

    @classmethod
    def from_pydantic(cls, user: UserInDB) -> "UserORM":
        return cls(
            name=user.name,
            hash=user.hash,
            role=user.role,
            disabled=user.disabled,
            google_sub=user.google_sub,
            email=user.email,
            email_verified=user.email_verified,
            picture=user.picture,
        )


class XUserORM(Base):
    __tablename__ = "xuser"

    name: Mapped[str] = mapped_column(primary_key=True)
    hash: Mapped[str]
