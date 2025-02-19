from typing import Annotated

import os

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel


postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_database = os.getenv("POSTGRES_DB")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{postgres_user}:{postgres_password}@localhost:5432/{postgres_database}",
)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]
