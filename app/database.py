from dotenv import load_dotenv
import os
from sqlmodel import create_engine

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_database = os.getenv("POSTGRES_DB")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{postgres_user}:{postgres_password}@localhost:5432/{postgres_database}",
)

engine = create_engine(DATABASE_URL)
