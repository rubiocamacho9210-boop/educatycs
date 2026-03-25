"""
Database connection and session management.

Supports SQLite for local development and PostgreSQL for production.
"""

from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import get_settings

settings = get_settings()


def normalize_database_url(database_url: str) -> str:
    """Normalize provider URLs so SQLAlchemy uses the intended driver."""
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://") and "+psycopg" not in database_url:
        parts = urlsplit(database_url)
        database_url = urlunsplit(
            ("postgresql+psycopg", parts.netloc, parts.path, parts.query, parts.fragment)
        )
    return database_url


DATABASE_URL = normalize_database_url(settings.database_url)

# SQLite requires check_same_thread=False for multi-threaded access.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=not DATABASE_URL.startswith("sqlite"),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


def get_db():
    """Dependency for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
