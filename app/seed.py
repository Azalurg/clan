import json
import random

from sqlmodel import select, Session

from app.database import engine
from app.models.champions import (
    Race,
    CharacterClass,
    Profession,
    Champion,
    Attribute,
)


def load_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_txt(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.readlines()


def seed_table(model, data):
    with Session(engine) as local_session:  # Use context manager for session
        for entry in data:
            if local_session.exec(
                select(model).where(model.name == entry["name"])
            ).first():
                continue
            print(entry)
            local_session.add(model(**entry))
        local_session.commit()


def create_random_champion(new_name):
    with Session(engine) as local_session:
        if local_session.exec(
            select(Champion).where(Champion.name == new_name)
        ).first():
            return

        races = local_session.exec(select(Race)).all()
        classes = local_session.exec(select(CharacterClass)).all()
        professions = local_session.exec(select(Profession)).all()

        race = random.choice(races)
        character_class = random.choice(classes)
        profession = random.choice(professions)

        experience = (
            random.randint(1, 25)
            * random.randint(1, 25)
            * random.randint(1, 25)
            * random.randint(1, 25)
        )

        champion = Champion(
            name=new_name,
            race_id=race.id,
            character_class_id=character_class.id,
            profession_id=profession.id,
            race=race,
            character_class=character_class,
            profession=profession,
            level=1,
            experience=experience,
        )

        champion.level_up()

        value = random.randint(1, 20)
        while champion.free_attribute_points > value:
            attribute = random.choice(list(Attribute))
            setattr(champion, attribute.value, getattr(champion, attribute.value) + 1)
            champion.free_attribute_points -= 1

        local_session.add(champion)
        local_session.commit()
        print(f"New champion {new_name}")


if __name__ == "__main__":
    # Load data and seed tables
    races_data = load_json("../data/races.json")
    seed_table(Race, races_data)

    classes_data = load_json("../data/classes.json")
    seed_table(CharacterClass, classes_data)

    professions_data = load_json("../data/professions.json")
    seed_table(Profession, professions_data)

    champions_names = load_txt("../data/raw/names.txt")

    random.shuffle(champions_names)

    for name in champions_names[:20]:
        create_random_champion(name.strip())
