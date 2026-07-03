from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from db.db_seeds import execute_seeds

from utility.utils import get_env_key

DATABASE_URL = get_env_key("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

def init_db():
    # Enable pgvector
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    create_tables()
    db = SessionLocal() 
    execute_seeds(db)
    db.close()
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()