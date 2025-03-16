from datetime import datetime
from typing import Optional, Type, Any, Dict
from uuid import UUID

from passlib.context import CryptContext
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.main import _TSQLModel

from app.models.shared import Entity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Clan(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    title: Optional[str] = None
    description: Optional[str] = None

    users: list["User"] = Relationship(back_populates="clan")
    items: list["Item"] = Relationship(back_populates="clan")
    warehouse: list["Warehouse"] = Relationship(back_populates="clan")
    champions: list["Champion"] = Relationship(back_populates="clan")


class User(Entity, table=True):
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=False)

    clan_id: Optional[UUID] = Field(default=None, foreign_key="clan.id", unique=True)
    clan: Optional[Clan] = Relationship(back_populates="users")


class ClanResponse(SQLModel, table=False):
    id: UUID
    name: str
    create_date: datetime
    age: str
    users_count: int
    champions_count: int

    @classmethod
    def from_orm(cls, obj: Clan):
        now = datetime.now()
        delta = now - obj.created_at

        years = delta.days // 365
        days = delta.days % 365
        hours = delta.seconds // 3600

        age = f"{years} year{'s' if years != 1 else ''} {days} day{'s' if days != 1 else ''} {hours} hour{'s' if hours != 1 else ''}"
        return cls(
            id=obj.id,
            name=obj.name,
            create_date=obj.created_at,
            age=age,
            users_count=len(obj.users),
            champions_count=len(obj.champions),
        )
