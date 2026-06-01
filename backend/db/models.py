from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from db.database import Base


class MovieVector(Base):
    __tablename__ = "movie_vectors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tmdb_id = Column(Integer, nullable=False)
    embedding = Column(Vector(1536))


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tmdb_id = Column(Integer)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    poster_path = Column(String, nullable=True, default=None)
    original_language = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    genre_ids = Column(ARRAY(Integer, dimensions=1), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(70), unique=True)
    password = Column(String(250))
    created_at = Column(DateTime)
