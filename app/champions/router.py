from fastapi import APIRouter
from sqlmodel import Session, select

from app.database import engine
from app.champions.models import Champion


router = APIRouter(prefix="/champions", tags=["champions"])


@router.get("/")
def get_champions():
    with Session(engine) as session:  # TODO: Move to service
        champions = session.exec(select(Champion).limit(10)).all()
    return champions
