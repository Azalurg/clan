from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.inventory import Resource
from app.models.shared import Entity
from app.models.users import Clan


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class MarketOffer(Entity, table=True):
    clan_id: UUID = Field(foreign_key="clan.id")
    resource_id: UUID = Field(foreign_key="resource.id")
    quantity: int = Field(ge=1, nullable=False)
    price_per_unit: int = Field(ge=1, nullable=False)

    clan: Clan = Relationship()
    resource: Resource = Relationship()


class Exchange(Entity, table=True):
    resource_id: UUID = Field(foreign_key="resource.id")
    price_per_unit: int = Field(ge=1, nullable=False)
    available_quantity: int = Field(ge=0, nullable=False)

    resource: Resource = Relationship()


class Transaction(Entity, table=True):
    resource_id: UUID = Field(foreign_key="resource.id")
    seller_clan_id: UUID = Field(foreign_key="clan.id", nullable=True)
    buyer_clan_id: UUID = Field(foreign_key="clan.id", nullable=True)
    quantity: int = Field(ge=1, nullable=False)
    price_per_unit: int = Field(ge=0, nullable=False)

    resource: Resource = Relationship()
