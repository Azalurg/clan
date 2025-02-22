from sqlmodel import Session, select

from app.models import User
from app.models import Clan, ClanWarehouse

def is_clan_name_in_db(session: Session, name: str) -> bool:
    return session.exec(select(Clan).where(Clan.name == name)).first() is not None

def create_clan(
    session: Session, user: User, clan_name: str
):
    if user.clan_id is not None:
        raise ValueError("User in already in a clan")

    if is_clan_name_in_db(session, clan_name):
        raise ValueError(f"Clan '{clan_name}' already exists")

    new_clan = Clan(name=clan_name)
    session.add(new_clan)
    session.commit()
    session.refresh(new_clan)

    user.clan_id = new_clan.id
    new_clan_warehouse = ClanWarehouse(clan_id=new_clan.id, resources={})

    session.add(user)
    session.add(new_clan_warehouse)
    session.commit()

    return new_clan

def get_clans(session: Session, limit: int = 20):
    clans = session.exec(select(Clan).limit(limit)).all()
    return clans

