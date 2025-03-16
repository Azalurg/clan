from uuid import UUID
from sqlmodel import Session, select

from app.models import Champion


def get_unaffiliated_champions(session: Session, limit: int = 20):
    return session.exec(select(Champion).where(Champion.clan_id == None).limit(limit)).all()


def get_clans_champions(session: Session, clan_id: UUID):
    return session.exec(select(Champion).where(Champion.clan_id == clan_id)).all()
