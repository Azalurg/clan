from fastapi import Depends, APIRouter


from app.models.users import User

from app.services.auth import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}
