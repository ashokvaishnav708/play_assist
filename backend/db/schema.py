"""SQLAlchemy ORM table definitions (the persistence model, distinct from
the Pydantic request/response models in models/)."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from pgvector.sqlalchemy import Vector
from db.database import Base
import uuid
from utility.utils import get_env_key

# Dimensionality of the embedding vectors stored per movie, used for
# similarity search; must match the embedding model configured in ai/llm.py.
VECTOR_SIZE = int(get_env_key("VECTOR_SIZE"))


class Movie(Base):
    """A movie record, including its TMDB metadata and precomputed embedding."""

    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    tmdb_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    poster_path = Column(String, nullable=True, default=None)
    original_language = Column(String, nullable=False)
    overview = Column(String, nullable=False)
    genre_types = Column(ARRAY(String, dimensions=1), nullable=False)
    # Vector embedding of the movie's text (title/overview/genres), used for
    # cosine-similarity search in MovieRepository.similarity_search.
    embedding = Column(Vector(VECTOR_SIZE))


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
    """An application user, including auth/session-related fields."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(70), unique=True)
    password = Column(String(250))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    # Incremented on logout to invalidate all previously issued JWTs for this
    # user (see AuthHandler / UserService.logout).
    token_version = Column(Integer, default=0, nullable=False)
    # favorite_movies = Column(ARRAY(UUID(as_uuid=True), dimensions=1), nullable=False)
    # favorites_tv_series = Column(ARRAY(UUID(as_uuid=True), dimensions=1), nullable=False)
