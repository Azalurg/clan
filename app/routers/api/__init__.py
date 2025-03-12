from fastapi import APIRouter

from app.routers.api.auth import router as auth_router
from app.routers.api.users import router as user_route
from app.routers.api.champions import router as champion_router
from app.routers.api.clans import router as clan_router
from app.routers.api.resources import router as resource_router
from app.routers.api.missions import router as missions_router

routers = [auth_router, champion_router, clan_router, missions_router, resource_router, user_route]

api_router = APIRouter()

for router in routers:
    api_router.include_router(router)
