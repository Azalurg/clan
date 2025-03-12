from fastapi import Depends, APIRouter

from app.database import SessionDep
from app.models.missions import Mission
from app.logic.missions import generate_random_mission


router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("/generate")
def generate_mission(session: SessionDep):
    new_mission = generate_random_mission(session)
    return {"mission": new_mission}
