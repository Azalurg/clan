from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from fastapi.responses import HTMLResponse

from app.database import engine
from app.models.champions import Champion

router = APIRouter(prefix="/champions", tags=["champions"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_champions():
    with Session(engine) as session:  # TODO: Move to service
        champions = session.exec(
            select(Champion)
            .order_by(Champion.level.desc())
            .options(
                selectinload(Champion.race),
                selectinload(Champion.champion_class),
                selectinload(Champion.profession),
            )
            .limit(10)
        ).all()

    return [
        {
            "name": champ.name,
            "level": champ.level,
            "race": champ.race.name,
            "class": champ.champion_class.name,
            "profession": champ.profession.name,
        }
        for champ in champions
    ]


@router.get("/templates", response_class=HTMLResponse)
def get_champions_list_templates(request: Request):
    context = {"champions": get_champions()}
    print(context)
    return templates.TemplateResponse(request=request, name="champions.j2", context=context)
