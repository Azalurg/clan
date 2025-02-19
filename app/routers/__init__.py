from app.routers.auth import router as auth_router
from app.routers.users import router as user_route
from app.routers.champions import router as champion_router


routers = [auth_router, user_route, champion_router]
