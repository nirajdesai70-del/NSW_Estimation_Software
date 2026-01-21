"""
Database Configuration
SQLAlchemy 2.0 style
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

# Ensure DATABASE_URL uses psycopg driver (postgresql+psycopg://)
# This is required for proper Alembic migration support
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://") and "+psycopg" not in database_url:
    # Convert postgresql:// to postgresql+psycopg:// if not already present
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

# Pool settings only for PostgreSQL (SQLite doesn't support them)
engine_kwargs: dict[str, object] = {
    "echo": settings.DATABASE_ECHO,
    "pool_pre_ping": True,
}

# Only add pool settings for PostgreSQL
if database_url.startswith("postgresql"):
    engine_kwargs.update(
        {
            "pool_size": 10,
            "max_overflow": 20,
        }
    )

engine = create_engine(database_url, **engine_kwargs)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 style declarative base for all models"""

    pass


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
