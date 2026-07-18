"""SQLAlchemy engine/session setup and FastAPI startup helpers."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from db.db_seeds import execute_seeds

from utility.utils import get_env_key

DATABASE_URL = get_env_key("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarative base every ORM model (db/schema.py) inherits from.
Base = declarative_base()


def create_tables():
    """Create any ORM-mapped tables that don't already exist."""
    Base.metadata.create_all(bind=engine)


def init_db():
    """App-startup routine: enable pgvector, create tables, and run seeds.

    Called once from the FastAPI lifespan handler in main.py.
    """
    # Enable pgvector
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    create_tables()
    db = SessionLocal()
    execute_seeds(db)
    db.close()


def get_db():
    """FastAPI dependency that yields a request-scoped DB session and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
