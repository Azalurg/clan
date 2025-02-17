import enum
from uuid import UUID

from sqlmodel import Field

from app.models import Entity

class ItemType(enum.Enum):
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

class Resource(Entity, table=True):
    name: str = Field(unique=True, nullable=False)

class Item(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    type: ItemType = Field(default=ItemType.weapon)
    parent_id: UUID | None = Field(default=None, foreign_key="item.id", nullable=True)
    main_resource_id: UUID | None = Field(default=None, foreign_key="resource.id", nullable=True)
    secondary_resource_id: UUID | None = Field(default=None, foreign_key="resource.id", nullable=True)

class Artefact(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    power: int = Field(ge=1, le=9999, default=100)
    type: ItemType = Field(default=ItemType.weapon)
    quality: ItemQuality = Field(default=ItemQuality.common)

    @property
    def score(self) -> int:
        item_quality_map = {
            ItemQuality.common: 1,
            ItemQuality.uncommon: 1.1,
            ItemQuality.rare: 1.2,
            ItemQuality.epic: 1.333,
            ItemQuality.magnificent: 1.5,
            ItemQuality.legendary: 2,
        }

        score = self.power * item_quality_map[self.quality]

        return int(score)
