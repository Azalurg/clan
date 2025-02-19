from datetime import datetime

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class Entity(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: datetime | None = Field(default=datetime.now(), nullable=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
