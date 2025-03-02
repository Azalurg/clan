from types import new_class

from fastapi import Depends, APIRouter

from app.database import SessionDep
from app.models.users import User
from app.models.clans import Clan
from app.routers.shared import handle_exceptions

from app.services.auth import get_current_user
from app.services.clans import create_clan, get_clans

router = APIRouter(prefix="/clans", tags=["clans"])


@router.get("/")
@handle_exceptions
def get_clans_list(session: SessionDep):
    clans = get_clans(session)

    return {"clans": clans}


@router.post("/")
@handle_exceptions
def crate_clan(
    name: str, session: SessionDep, current_user: User = Depends(get_current_user)
):
    new_clan = create_clan(session, current_user, name)

    return {"message": f"Clan '{name}' created", "clan_id": new_clan.id}
