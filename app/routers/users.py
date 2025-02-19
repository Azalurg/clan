from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_session, SessionDep
from app.models.users import User
from app.services.users import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)

from app.services.auth import (
    authenticate_user,
    access_token_expire,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register(username: str, email: str, password: str, session: SessionDep):
    if get_user_by_username(session, username) or get_user_by_email(session, email):
        raise HTTPException(status_code=400, detail="Username or email already taken")
    user = create_user(session, username, email, password)
    return {"msg": "User created", "id": user.id}


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=access_token_expire)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}


@router.get("/secure-data")
def get_secure_data(current_user: User = Depends(get_current_user)):
    return {"message": "Access", "user": current_user.username}
