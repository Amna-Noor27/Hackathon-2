from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with appropriate settings for Neon Serverless PostgreSQL
engine = create_engine(
    DATABASE_URL,
    # For PostgreSQL
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection in FastAPI.
    """
    with Session(engine) as session:
        yield session