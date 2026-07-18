"""Data-access layer for the movies table."""

from .base import BaseRepository
from db.schema import Movie
from models.movie import MovieCreateRequest
from uuid import UUID
from typing import List


class MovieRepository(BaseRepository):
    """CRUD and query operations for Movie rows, including vector similarity search."""

    def create_movie(self, movie_data: MovieCreateRequest, embedding: List[float]):
        """Insert a new movie row along with its precomputed embedding."""

        new_movie = Movie(
            embedding=embedding, **movie_data.model_dump(exclude_none=True)
        )

        self._session.add(new_movie)
        self._session.commit()
        self._session.refresh(new_movie)

        return new_movie

    def movie_exist_by_tmdb_id(self, tmdb_id: int) -> bool:
        """Return True if a movie with the given TMDB id already exists."""
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        return bool(movie)

    def get_movie_by_tmdb_id(self, tmdb_id: str) -> List[Movie]:
        """Fetch a movie by its TMDB id, or None if not found."""
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        return movie

    def get_movie_by_id(self, id: UUID) -> Movie | None:
        """Fetch a movie by its internal UUID, or None if not found."""
        movie = self._session.query(Movie).filter_by(id=id).first()
        return movie

    def get_movies_by_range(self, offset: int, limit: int = 20) -> List[Movie]:
        """Fetch a page of movies ordered by id, for simple pagination."""
        movies = (
            self._session.query(Movie)
            .order_by(Movie.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return movies

    def similarity_search(
        self, query_embedding: List[float], limit: int = 20
    ) -> List[Movie]:
        """Return the movies whose embeddings are closest (cosine distance) to the query embedding."""
        movies = (
            self._session.query(Movie)
            .order_by(Movie.embedding.cosine_distance(query_embedding))
            .limit(limit)
            .all()
        )
        return movies
