from sqlmodel import Session

from app.models import User
from app.models import Clan, ClanWarehouse


def create_clan(
    session: Session, user: User, clan_name: str
):  # TODO: Add check for user and clan name
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
