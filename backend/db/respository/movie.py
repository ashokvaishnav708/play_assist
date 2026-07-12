from .base import BaseRepository
from db.schema import Movie
from models.movie import MovieCreateRequest
from uuid import UUID
from typing import List


class MovieRepository(BaseRepository):
    def create_movie(self, movie_data: MovieCreateRequest, embedding: List[float]):

        new_movie = Movie(
            embedding=embedding, **movie_data.model_dump(exclude_none=True)
        )

        self._session.add(new_movie)
        self._session.commit()
        self._session.refresh(new_movie)

        return new_movie

    def movie_exist_by_tmdb_id(self, tmdb_id: int) -> bool:
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        return bool(movie)

    def get_movie_by_tmdb_id(self, tmdb_id: str) -> List[Movie]:
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        return movie

    def get_movie_by_id(self, id: UUID) -> Movie | None:
        movie = self._session.query(Movie).filter_by(id=id).first()
        return movie

    def get_movies_by_range(self, offset: int, limit: int = 20) -> List[Movie]:
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
        movies = (
            self._session.query(Movie)
            .order_by(Movie.embedding.cosine_distance(query_embedding))
            .limit(limit)
            .all()
        )
        return movies
