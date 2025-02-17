from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import engine
from app.players.models import Player


router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
def get_players():
    with Session(engine) as session:  # TODO: Move to service
        players = session.exec(select(Player).limit(10)).all()
    return players
