import enum
from uuid import UUID

from sqlmodel import Field, Column, JSON

from app.models.shared import Entity


class ItemType(enum.Enum):
    material = "material"
    weapon = "weapon"
    armor = "armor"
    potion = "potion"
    scroll = "scroll"
    jewelry = "jewelry"
    rod = "rod"
    wand = "wand"
    orb = "orb"
    tome = "tome"
    grimoire = "grimoire"
    talisman = "talisman"
    clothing = "clothing"
    extras = "extras"
    instrument = "instrument"
    tool = "tool"

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
    item_type: ItemType = Field(default=ItemType.material)
    recipe: dict[UUID, int] | None = Field(default=None, sa_column=Column(JSON))
    base_price: int = Field(ge=1, le=9999, default=1)

    @property
    def price (self) -> int:
        price = self.base_price
        for item_id, count in self.recipe.items():
            item = self.session.get(Item, item_id)
            price += item.price * count
        return price


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