from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from app.models import Champion
from app.models.shared import Entity
from app.models.users import Clan


class Mission(Entity, table=True):
    title: str = Field(unique=True, nullable=False)
    description: Optional[str] = None
    level: int = Field(ge=1, le=9999, default=1)

    total_duration: int = Field(ge=1, le=100, default=1)  # W minutach lub godzinach
    start_time: Optional[datetime] = Field(default=None)  # Kiedy misja się zaczęła
    end_time: Optional[datetime] = Field(default=None)  # Kiedy się zakończy
    active: bool = Field(default=False)

    max_champions: int = Field(ge=1, le=10, default=1)
    min_champions: int = Field(ge=1, le=10, default=1)

    clan_id: UUID = Field(foreign_key="clan.id")
    clan: Clan = Relationship()

    participants: List["MissionParticipant"] = Relationship(back_populates="mission")
    rewards: List["MissionReward"] = Relationship(back_populates="mission")


class MissionParticipant(Entity, table=True):
    mission_id: UUID = Field(foreign_key="mission.id")
    champion_id: UUID = Field(foreign_key="champion.id")

    mission: Mission = Relationship(back_populates="participants")
    champion: Champion = Relationship()


class MissionReward(Entity, table=True):
    mission_id: UUID = Field(foreign_key="mission.id")
    money: int = Field(ge=0, default=0)
    experience: int = Field(ge=0, default=0)
    luck: int = Field(ge=0, default=0)
    items: Optional[Dict[UUID, int]] = Field(
        default=None, sa_column=Column(JSON)
    )  # Przedmioty jako słownik {item_id: ilość}

    mission: Mission = Relationship(back_populates="rewards")
