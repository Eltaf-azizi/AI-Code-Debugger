"""
Database Connection
SQLAlchemy database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

# Create engine
engine = None
SessionLocal = None
Base = declarative_base()


def init_db():
    """Initialize database connection."""
    global engine, SessionLocal
    
    if settings.DATABASE_URL:
        engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            pool_pre_ping=True
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    else:
        # Use SQLite for development
        engine = create_engine(
            "sqlite:///./ai_code_assistant.db",
            echo=settings.DATABASE_ECHO
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    
    # Create tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Database session
    """
    if SessionLocal is None:
        init_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize on import
try:
    init_db()
except Exception:
    pass  # Ignore if database is not available
