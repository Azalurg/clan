from uuid import UUID

from sqlmodel import Session, select

from app.models import User
from app.models import Clan
from app.services.champions import get_champion_by_id


def is_clan_name_in_db(session: Session, name: str) -> bool:
    return session.exec(select(Clan).where(Clan.name == name)).first() is not None


def create_clan(session: Session, user: User, clan_name: str):  # TODO: Check this function
    if user.clan_id is not None:
        raise ValueError("User in already in a clan")

    if is_clan_name_in_db(session, clan_name):
        raise ValueError(f"Clan '{clan_name}' already exists")

    new_clan = Clan(name=clan_name)
    session.add(new_clan)
    session.commit()
    session.refresh(new_clan)

    user.clan_id = new_clan.id

    session.add(user)
    session.commit()

    return new_clan


def get_clans(session: Session, limit: int = 20):
    clans = session.exec(select(Clan).limit(limit)).all()
    return clans


def get_clan_by_id(session: Session, clan_id: UUID):
    return session.exec(select(Clan).where(Clan.id == clan_id)).first()


def assign_champion_to_clan(session: Session, champion_id: UUID, clan_id: UUID):
    champion = get_champion_by_id(session, champion_id)

    if champion.clan_id is not None:
        raise ValueError(f"Champion is already in a clan {champion.clan.name}")

    champion.clan_id = clan_id
    session.add(champion)
    session.commit()
    session.refresh(champion)

    return champion
