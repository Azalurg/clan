from sqlmodel import Session, select
from passlib.context import CryptContext

from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).one_or_none()


def get_user_by_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).one_or_none()


def create_user(session: Session, username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
