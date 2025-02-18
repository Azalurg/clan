from fastapi import APIRouter
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
import json

from app.database import engine
from app.champions.models import Champion, Race

router = APIRouter(prefix="/champions", tags=["champions"])


@router.get("/")
def get_champions():
    with Session(engine) as session:  # TODO: Move to service
        champions = session.exec(
            select(Champion)
            .order_by(Champion.level.desc())
            .options(
                selectinload(Champion.race),
                selectinload(Champion.character_class),
                selectinload(Champion.profession),
            )
            .limit(10)
        ).all()

    return [
        {
            "name": champ.name,
            "level": champ.level,
            "race": champ.race.name,
            "class": champ.character_class.name,
            "profession": champ.profession.name,
        }
        for champ in champions
    ]
