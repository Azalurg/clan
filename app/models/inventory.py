import enum
from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Column, JSON, Relationship

from app.models.shared import Entity
from app.models.users import Clan


class ItemType(enum.Enum):
    MATERIAL = "MATERIAL"
    MELEE_WEAPON = "MELEE_WEAPON"
    RANGED_WEAPON = "RANGED_WEAPON"
    ARMOR = "ARMOR"
    CLOTHING = "CLOTHING"
    POTION = "POTION"
    SCROLL = "SCROLL"
    MAGIC_ITEM = "MAGIC_ITEM"
    JEWELRY = "JEWELRY"
    TOOL = "TOOL"
    INSTRUMENT = "INSTRUMENT"
    MISC = "MISC"


class ItemQuality(enum.Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    MAGNIFICENT = "MAGNIFICENT"
    LEGENDARY = "LEGENDARY"
    ARTEFACT = "ARTEFACT"


class Resource(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    item_type: ItemType = Field(default=ItemType.MATERIAL)
    recipe: dict[UUID, int] | None = Field(default=None, sa_column=Column(JSON))
    base_price: int = Field(ge=1, le=9999, default=1)

    @property
    def price(self) -> int:
        price = self.base_price
        for item_id, count in self.recipe.items():
            item = self.session.get(Item, item_id)
            price += item.price * count
        return price


class Warehouse(Entity, table=True):
    clan_id: UUID = Field(foreign_key="clan.id")
    resource_id: UUID = Field(foreign_key="resource.id")
    quantity: int = Field(ge=0, nullable=False)

    clan: Optional["Clan"] = Relationship(back_populates="warehouse")  # Add this line

    __table_args__ = (UniqueConstraint("clan_id", "resource_id"),)


class Item(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = Field(default=None)
    power: int = Field(ge=1, le=9999, default=100)
    type: ItemType = Field(default=ItemType.MISC)
    quality: ItemQuality = Field(default=ItemQuality.COMMON)

    clan_id: UUID = Field(foreign_key="clan.id")
    clan: Clan = Relationship(back_populates="items")

    @property
    def score(self) -> int:
        item_quality_map = {
            ItemQuality.COMMON: 1,
            ItemQuality.UNCOMMON: 1.2,
            ItemQuality.RARE: 1.5,
            ItemQuality.EPIC: 2,
            ItemQuality.MAGNIFICENT: 2.5,
            ItemQuality.LEGENDARY: 3.5,
            ItemQuality.ARTEFACT: 5,
        }

        score = self.power * item_quality_map[self.quality]

        return int(score)
