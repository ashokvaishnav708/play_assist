from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from pgvector.sqlalchemy import Vector
from db.database import Base
import uuid


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    tmdb_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    poster_path = Column(String, nullable=True, default=None)
    original_language = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    genre_ids = Column(ARRAY(Integer, dimensions=1), nullable=False)
    embedding = Column(Vector(3072))

# TV Series will be implemented later
# class TVSeries(Base):
#     __tablename__ = "tv_Series"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     tmdb_id = Column(Integer)
#     title = Column(String, nullable=False)
#     release_date = Column(String, nullable=False)
#     poster_path = Column(String, nullable=True, default=None)
#     original_language = Column(String, nullable=False)
#     overview = Column(String, nullable=False)
#     genre_ids = Column(ARRAY(Integer, dimensions=1), nullable=False)



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(70), unique=True)
    password = Column(String(250))
    created_at = Column(DateTime)
    favorite_movies = Column(ARRAY(UUID(as_uuid=True), dimensions=1), nullable=False)
    # favorites_tv_series = Column(ARRAY(UUID(as_uuid=True), dimensions=1), nullable=False)
