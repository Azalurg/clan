import json
import random

from sqlmodel import select, Session

from app.database import engine
from app.players.models import (
    Race,
    CharacterClass,
    Profession,
    Player,
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


def emulate_data(raw_data):
    return [
        {
            "name": profession,
            "rarity": random.randint(1, 10),
            "main_attribute": random.choice(list(Attribute)),
            "secondary_attribute": random.choice(list(Attribute)),
        }
        for profession in raw_data
    ]


def create_random_player(new_name, races_in, classes_in, professions_in):
    with Session(engine) as session:
        if session.exec(select(Player).where(Player.name == new_name)).first():
            return

        race = random.choice(races_in)
        character_class = random.choice(classes_in)
        profession = random.choice(professions_in)

        experience = (
            random.randint(1, 20) * random.randint(1, 20) * random.randint(1, 20)
        )

        player = Player(
            name=new_name,
            race_id=race.id,
            character_class_id=character_class.id,
            profession_id=profession.id,
            level=1,
            experience=experience,
        )

        player.level_up()

        session.add(player)
        session.commit()
        print(f"New player {new_name}")


if __name__ == "__main__":
    # Load data and seed tables
    races_data = load_json("../data/races.json")
    seed_table(Race, races_data)

    classes_data = load_json("../data/classes.json")
    seed_table(CharacterClass, classes_data)

    professions_data = load_txt("../data/raw/professions.txt")
    emulate_professions = emulate_data(professions_data)
    seed_table(Profession, emulate_professions)

    players_names = load_txt("../data/raw/names.txt")

    with Session(engine) as session:
        races = session.exec(select(Race)).all()
        classes = session.exec(select(CharacterClass)).all()
        professions = session.exec(select(Profession)).all()

    for name in players_names:
        create_random_player(name.strip(), races, classes, professions)
