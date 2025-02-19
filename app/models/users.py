# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt

from passlib.context import CryptContext
from sqlmodel import Field, Relationship
from uuid import UUID

from app.models.shared import Entity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Entity, table=True):
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=False)

    # clan_id: UUID | None = Field(foreign_key="clan.id")
    # clan: Clan = Relationship()

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)
