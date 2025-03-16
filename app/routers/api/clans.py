from uuid import UUID

from fastapi import Depends, APIRouter

from app.database import SessionDep
from app.models import User
from app.models.users import ClanResponse
from app.routers.shared import handle_exceptions

from app.services.auth import get_current_user
from app.services.clans import create_clan, get_clans, assign_champion_to_clan, get_clan_by_id

router = APIRouter(prefix="/clans", tags=["clans"])


@router.get("/")
@handle_exceptions
def get_clans_list(session: SessionDep):
    clans = get_clans(session)

    return clans


@router.get("/my", response_model=ClanResponse)
@handle_exceptions
def get_users_clan(session: SessionDep, current_user: User = Depends(get_current_user)):
    # clan = get_clan_by_id(session, current_user.clan_id)
    print(current_user.clan)
    response = ClanResponse.from_orm(current_user.clan)
    print(response)
    return response


@router.post("/")
@handle_exceptions
def crate_clan(name: str, session: SessionDep, current_user: User = Depends(get_current_user)):
    new_clan = create_clan(session, current_user, name)

    return {"message": f"Clan '{name}' created", "clan_id": new_clan.id}


@router.post("/assign_champion")
@handle_exceptions
def assign_champion(
    champion_id: UUID, session: SessionDep, current_user: User = Depends(get_current_user)
):
    champion = assign_champion_to_clan(session, champion_id, current_user.clan_id)
    return {"message": f"Champion '{champion.name}' assigned to clan '{current_user.clan.name}'"}
