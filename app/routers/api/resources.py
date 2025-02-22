from fastapi import APIRouter

from app.database import SessionDep
from app.routers.shared import handle_exceptions
from app.services.recources import get_resources

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/")
@handle_exceptions
def get_resources_list(session: SessionDep):
    resources = get_resources(session)

    return {"resources": resources}