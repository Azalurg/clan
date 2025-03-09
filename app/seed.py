import json
import random
import argparse

import numpy as np
from dotenv import load_dotenv
from sqlmodel import select, Session

load_dotenv()

from app.database import engine
from app.models.champions import (
    Race,
    ChampionClass,
    Profession,
    Champion,
    Attribute,
)
from app.models import Resource


def load_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_txt(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.readlines()


def seed_table(model, data):
    with Session(engine) as local_session:
        for entry in data:
            if local_session.exec(select(model).where(model.name == entry["name"])).first():
                continue
            print(entry)
            local_session.add(model(**entry))
        local_session.commit()


def create_random_champion(new_name):
    with Session(engine) as local_session:
        if local_session.exec(select(Champion).where(Champion.name == new_name)).first():
            return

        races = local_session.exec(select(Race)).all()
        classes = local_session.exec(select(ChampionClass)).all()
        professions = local_session.exec(select(Profession)).all()

        race = random.choice(races)
        champion_class = random.choice(classes)
        profession = random.choice(professions)

        mu = 0
        sigma = 25000

        experience = int(abs(np.random.normal(mu, sigma)))

        champion = Champion(
            name=new_name,
            race_id=race.id,
            champion_class_id=champion_class.id,
            profession_id=profession.id,
            race=race,
            champion_class=champion_class,
            profession=profession,
            level=1,
            experience=experience,
        )

        champion.level_up()

        value = random.randint(1, 20)
        while champion.free_attribute_points > value:
            attribute = random.choice(list(Attribute))
            a = attribute.value.lower()
            setattr(champion, a, getattr(champion, a) + 1)
            champion.free_attribute_points -= 1

        local_session.add(champion)
        local_session.commit()
        print(f"New champion {new_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--champions", type=int, help="Number of champions to create")
    args = parser.parse_args()

    races_data = load_json("../data/races.json")
    classes_data = load_json("../data/classes.json")
    professions_data = load_json("../data/professions.json")
    resources_data = load_json("../data/resources.json")

    seed_table(Race, races_data)
    seed_table(ChampionClass, classes_data)
    seed_table(Profession, professions_data)
    seed_table(Resource, resources_data)

    if args.champions:
        champions_names = load_txt("../data/raw/names.txt")
        random.shuffle(champions_names)

        for name in champions_names[: args.champions]:
            create_random_champion(name.strip())
