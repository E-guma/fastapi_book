"""SQLAlchemy ORM models."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from model.creature import Creature
from model.explorer import Explorer
from model.user import UserInDB


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class CreatureORM(Base):
    __tablename__ = "creature"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    country: Mapped[str] = mapped_column(String)
    area: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    aka: Mapped[str] = mapped_column(String)

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

    name: Mapped[str] = mapped_column(String, primary_key=True)
    country: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

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

    name: Mapped[str] = mapped_column(String, primary_key=True)
    hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")
    disabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def to_pydantic(self) -> UserInDB:
        return UserInDB(
            name=self.name,
            hash=self.hash,
            role=self.role,
            disabled=self.disabled,
        )

    @classmethod
    def from_pydantic(cls, user: UserInDB) -> "UserORM":
        return cls(
            name=user.name,
            hash=user.hash,
            role=user.role,
            disabled=user.disabled,
        )


class XUserORM(Base):
    __tablename__ = "xuser"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    hash: Mapped[str] = mapped_column(String, nullable=False)
