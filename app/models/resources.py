import enum
from uuid import UUID

from sqlmodel import Field, Column, JSON

from app.models.shared import Entity


class ItemType(enum.Enum):
    resource = "resource"
    weapon = "weapon"
    armor = "armor"
    potion = "potion"
    scroll = "scroll"
    ring = "ring"
    amulet = "amulet"
    rod = "rod"
    wand = "wand"
    staff = "staff"
    orb = "orb"
    tome = "tome"
    grimoire = "grimoire"
    talisman = "talisman"


class ItemQuality(enum.Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    epic = "epic"
    magnificent = "magnificent"
    legendary = "legendary"
    artefact = "artefact"


class Resource(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    item_type: ItemType = Field(default=ItemType.resource)
    recipe: dict[UUID, int] | None = Field(default=None, sa_column=Column(JSON))


class Item(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    power: int = Field(ge=1, le=9999, default=100)
    type: ItemType = Field(default=ItemType.weapon)
    quality: ItemQuality = Field(default=ItemQuality.common)

    @property
    def score(self) -> int:
        item_quality_map = {
            ItemQuality.common: 1,
            ItemQuality.uncommon: 1.2,
            ItemQuality.rare: 1.4,
            ItemQuality.epic: 1.6,
            ItemQuality.magnificent: 1.8,
            ItemQuality.legendary: 2,
            ItemQuality.artefact: 3,
        }

        score = self.power * item_quality_map[self.quality]

        return int(score)
