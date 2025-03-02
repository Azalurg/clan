import enum
from uuid import UUID

from sqlmodel import Field, Column, JSON, Relationship

from app.models import Clan
from app.models.shared import Entity

class Mission(Entity, table=True):
    title: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    level: int = Field(ge=1, le=9999, default=1)
    reward_money: int = Field(ge=1, le=9999, default=1)
    reward_exp: int = Field(ge=1, le=9999, default=1)
    reward_luck: int = Field(ge=1, le=9999, default=1)
    total_duration: int = Field(ge=1, le=100, default=1)
    duration: int = Field(ge=1, le=100, default=1)
    active: bool = Field(default=False)
    max_champions: int = Field(ge=1, le=10, default=1)
    min_champions: int = Field(ge=1, le=10, default=1)
    max_items: int = Field(ge=1, le=10, default=1)

    clan_id: UUID = Field(foreign_key="clan.id")

    clan: Clan = Relationship()
