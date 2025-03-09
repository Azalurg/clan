import enum
from typing import Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from app.models.shared import Entity


class Attribute(enum.Enum):
    STRENGTH = "STRENGTH"
    DEXTERITY = "DEXTERITY"
    CONSTITUTION = "CONSTITUTION"
    INTELLIGENCE = "INTELLIGENCE"
    WISDOM = "WISDOM"
    CHARISMA = "CHARISMA"


class AttributesMixin:
    strength: int = Field(default=1, ge=1)
    dexterity: int = Field(default=1, ge=1)
    constitution: int = Field(default=1, ge=1)
    intelligence: int = Field(default=1, ge=1)
    wisdom: int = Field(default=1, ge=1)
    charisma: int = Field(default=1, ge=1)


class PropertiesMixin:
    name: str = Field(unique=True)
    description: str | None = Field(default=None, nullable=True)
    rarity: int = Field(ge=1, le=10, default=2)
    main_attribute: Attribute = Field(default=Attribute.STRENGTH)
    secondary_attribute: Attribute = Field(default=Attribute.DEXTERITY)


class Race(Entity, PropertiesMixin, table=True):
    pass


class ChampionClass(Entity, PropertiesMixin, table=True):
    pass


class Profession(Entity, PropertiesMixin, table=True):
    pass


class Champion(Entity, AttributesMixin, table=True):
    name: str = Field(unique=True)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    level: int = Field(default=1, ge=1)
    experience: int = Field(default=0, ge=0)
    experience_to_next_level: int = Field(default=10, ge=1)
    free_attribute_points: int = Field(default=1, ge=0)

    race_id: Optional[UUID] = Field(default=None, foreign_key="race.id")
    champion_class_id: Optional[UUID] = Field(default=None, foreign_key="championclass.id")
    profession_id: Optional[UUID] = Field(default=None, foreign_key="profession.id")
    clan_id: Optional[UUID] = Field(default=None, foreign_key="clan.id")
    mission_id: Optional[UUID] = Field(default=None, foreign_key="mission.id")

    race: Optional["Race"] = Relationship()
    champion_class: Optional["ChampionClass"] = Relationship()
    profession: Optional["Profession"] = Relationship()
    clan: Optional["Clan"] = Relationship(back_populates="champions")

    def gain_experience(self, exp: int):
        self.experience += exp
        self.level_up()

    def level_up(self):
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level += 1

            if self.level % 10 == 0:
                self.free_attribute_points += 10 + self.level // 100
            else:
                self.free_attribute_points += 5

            main_attributes = [
                self.race.main_attribute.value,
                self.champion_class.main_attribute.value,
                self.profession.main_attribute.value,
            ]
            secondary_attributes = [
                self.race.secondary_attribute.value,
                self.champion_class.secondary_attribute.value,
                self.profession.secondary_attribute.value,
            ]

            for attribute in main_attributes:
                a = attribute.lower()
                setattr(self, a, getattr(self, a) + 2)

            for attribute in secondary_attributes:
                a = attribute.lower()
                setattr(self, a, getattr(self, a) + 1)

            if self.level <= 70:
                self.experience_to_next_level += self.level * 2 + 7
            elif self.level <= 150:
                self.experience_to_next_level += self.level * 5 + 643
            else:
                self.experience_to_next_level += self.level * 9 + 5465
