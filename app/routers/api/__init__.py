from fastapi import APIRouter

from app.routers.api.auth import router as auth_router
from app.routers.api.users import router as user_route
from app.routers.api.champions import router as champion_router
from app.routers.api.clans import router as clan_router
from app.routers.api.resources import router as resource_router

routers = [auth_router, user_route, champion_router, clan_router, resource_router]

api_router = APIRouter()

for router in routers:
    api_router.include_router(router)
