import enum
from uuid import UUID

from sqlmodel import Field, Relationship
from app.models import Entity


class Attribute(enum.Enum):
    strength = "strength"
    dexterity = "dexterity"
    constitution = "constitution"
    intelligence = "intelligence"
    wisdom = "wisdom"
    charisma = "charisma"


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


class Race(Entity, AttributesMixin, PropertiesMixin, table=True):
    pass


class CharacterClass(Entity, AttributesMixin, PropertiesMixin, table=True):
    pass


class Profession(Entity, PropertiesMixin, table=True):
    main_attribute: Attribute = Field(default=Attribute.strength)
    secondary_attribute: Attribute = Field(default=Attribute.dexterity)


class Background(Entity, PropertiesMixin, table=True):
    main_attribute: Attribute = Field(default=Attribute.strength)
    secondary_attribute: Attribute = Field(default=Attribute.dexterity)


class Player(Entity, AttributesMixin, table=True):
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
    background_id: UUID | None = Field(
        default=None, foreign_key="background.id", nullable=True
    )

    race: Race = Relationship()
    character_class: CharacterClass = Relationship()
    profession: Profession = Relationship()
    background: Background = Relationship()

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
            if self.level <= 70:
                self.experience_to_next_level += self.level * 2 + 7
            elif self.level <= 150:
                self.experience_to_next_level += self.level * 5 + 643
            else:
                self.experience_to_next_level += self.level * 9 + 5465
