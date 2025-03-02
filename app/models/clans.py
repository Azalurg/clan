from uuid import UUID

from sqlmodel import Field, Relationship, Field, Column, JSON

# from app.models.champions import Champion
# from app.models.items import Item
# from app.models.missions import Mission
# from app.models import User
from app.models.shared import Entity


class ClanWarehouse(Entity, table=True):
    clan_id: UUID = Field(foreign_key="clan.id", unique=True)
    resources: dict[UUID, int] = Field(default=None, sa_column=Column(JSON))


class Clan(Entity, table=True):
    name: str = Field(unique=True, nullable=False)
    title: str | None
    description: str | None

    clan_warehouse: ClanWarehouse = Relationship()

    # champions: list[Champion] = Relationship()
    # missions: list[Mission] = Relationship()
    # items: list[Item] = Relationship()
