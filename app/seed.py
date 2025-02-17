import json
import random

from sqlmodel import select, Session

from app.database import engine
from app.champions.models import (
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
    with Session(engine) as session:  # Use context manager for session
        for entry in data:
            if session.exec(select(model).where(model.name == entry["name"])).first():
                continue
            print(entry)
            session.add(model(**entry))
        session.commit()


def create_random_champion(new_name, races_in, classes_in, professions_in):
    with Session(engine) as session:
        if session.exec(select(Champion).where(Champion.name == new_name)).first():
            return

        race = random.choice(races_in)
        character_class = random.choice(classes_in)
        profession = random.choice(professions_in)

        experience = (
            random.randint(1, 20) * random.randint(1, 20) * random.randint(1, 20)
        )

        champion = Champion(
            name=new_name,
            race_id=race.id,
            character_class_id=character_class.id,
            profession_id=profession.id,
            level=1,
            experience=experience,
        )

        champion.level_up()

        value = random.randint(1, 20)
        while champion.free_attribute_points > value:
            attribute = random.choice(list(Attribute))
            pass  # TODO: Finish it

        session.add(champion)
        session.commit()
        print(f"New champion {new_name}")


if __name__ == "__main__":
    # Load data and seed tables
    races_data = load_json("../data/races.json")
    seed_table(Race, races_data)

    classes_data = load_json("../data/classes.json")
    seed_table(CharacterClass, classes_data)

    professions_data = load_json("../data/raw/professions.txt")
    seed_table(Profession, professions_data)

    champions_names = load_txt("../data/raw/names.txt")

    with Session(engine) as session:
        races = session.exec(select(Race)).all()
        classes = session.exec(select(CharacterClass)).all()
        professions = session.exec(select(Profession)).all()

    for name in champions_names:
        create_random_champion(name.strip(), races, classes, professions)
