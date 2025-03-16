from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from sqlmodel import select
from fastapi.responses import HTMLResponse

from app.database import engine, SessionDep
from app.models import User
from app.models.champions import Champion, ChampionResponse
from app.services.auth import get_current_user
from app.services.champions import get_unaffiliated_champions, get_clans_champions

router = APIRouter(prefix="/champions", tags=["champions"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_model=list[ChampionResponse])
def get_champions(session: SessionDep):
    champions = session.exec(select(Champion).limit(20)).all()
    response = [ChampionResponse.from_orm(champ) for champ in champions]
    return response


@router.get("/unaffiliated", response_model=list[ChampionResponse])
def get_unaffiliated_champions_list(session: SessionDep):
    champions = get_unaffiliated_champions(session)
    response = [ChampionResponse.from_orm(champ) for champ in champions]
    return response


@router.get("/my_clan")
def get_my_clan_champions_list(session: SessionDep, current_user: User = Depends(get_current_user)):
    clan_id = current_user.clan_id
    if clan_id is None:
        raise HTTPException(status_code=404, detail="User is not in a clan")

    champions = get_clans_champions(session, clan_id)
    response = [ChampionResponse.from_orm(champ) for champ in champions]

    return response


@router.get("/templates", response_class=HTMLResponse)
def get_champions_list_templates(request: Request):
    context = {"champions": get_champions()}
    return templates.TemplateResponse(request=request, name="champions.j2", context=context)
