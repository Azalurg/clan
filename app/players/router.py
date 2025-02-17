from fastapi import APIRouter, Depends

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/")
def get_players():
    players = [{"id": 1, "name": "admin", "lever": 10}]
    return players
