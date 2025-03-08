from typing import Optional
from uuid import UUID

from passlib.context import CryptContext
from sqlmodel import Field, Relationship

from app.models.shared import Entity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Clan(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    title: Optional[str] = None
    description: Optional[str] = None

    users: list["User"] = Relationship(back_populates="clan")
    items: list["Item"] = Relationship(back_populates="clan")
    warehouse: list["Warehouse"] = Relationship(back_populates="clan")


class User(Entity, table=True):
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=False)

    clan_id: Optional[UUID] = Field(default=None, foreign_key="clan.id", unique=True)
    clan: Optional[Clan] = Relationship(back_populates="users")
