# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords

from passlib.context import CryptContext
from sqlmodel import Field, Relationship
from uuid import UUID

from app.models import Entity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Player(Entity, table=True):
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    disabled: bool = Field(default=True)

    # clan_id: UUID | None = Field(foreign_key="clan.id")
    #
    # clan: Clan = Relationship()

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)
