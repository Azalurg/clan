import enum
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


class CharacterClass(Entity, PropertiesMixin, table=True):
    pass


class Profession(Entity, PropertiesMixin, table=True):
    pass


class Champion(Entity, AttributesMixin, table=True):
    name: str = Field(unique=True)
    title: str | None = Field(default=None, nullable=True)
    description: str | None = Field(default=None, nullable=True)
    level: int = Field(default=1, ge=1)
    experience: int = Field(default=0, ge=0)
    experience_to_next_level: int = Field(default=10, ge=1)
    free_attribute_points: int = Field(default=1, ge=0)

    race_id: UUID | None = Field(default=None, foreign_key="race.id", nullable=True)
    character_class_id: UUID | None = Field(
        default=None, foreign_key="characterclass.id", nullable=True
    )
    profession_id: UUID | None = Field(
        default=None, foreign_key="profession.id", nullable=True
    )
    clan_id: UUID | None = Field(default=None, foreign_key="clan.id", nullable=True)
    mission_id: UUID | None = Field(default=None, foreign_key="mission.id", nullable=True)

    race: Race = Relationship()
    character_class: CharacterClass = Relationship()
    profession: Profession = Relationship()

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
                self.character_class.main_attribute.value,
                self.profession.main_attribute.value,
            ]
            secondary_attributes = [
                self.race.secondary_attribute.value,
                self.character_class.secondary_attribute.value,
                self.profession.secondary_attribute.value,
            ]

            for attribute in main_attributes:
                setattr(self, attribute, getattr(self, attribute) + 2)

            for attribute in secondary_attributes:
                setattr(self, attribute, getattr(self, attribute) + 1)

            if self.level <= 70:
                self.experience_to_next_level += self.level * 2 + 7
            elif self.level <= 150:
                self.experience_to_next_level += self.level * 5 + 643
            else:
                self.experience_to_next_level += self.level * 9 + 5465
