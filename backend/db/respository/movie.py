from .base import BaseRepository
from db.models import Movie
from models.movie import MovieCreateRequest
from sqlalchemy.orm import Query


class MovieRepository(BaseRepository):
    def create_movie(self, movie_data: MovieCreateRequest):
        new_movie = Movie(**movie_data.model_dump(exclude_none=True))

        self._session.add(new_movie)
        self._session.commit()
        self._session.refresh(new_movie)

        return new_movie
    
    def movie_exist_by_tmdb_id(self, tmdb_id: int) -> bool:
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        return bool(movie)
    
    def get_movie_by_tmdb_id(self, tmdb_id: str) -> Query[Movie]:
        movie = self._session.query(Movie).filter_by(tmdb_id=tmdb_id)
        return movie
    
    def get_movie_by_id(self, id: int) -> Movie | None:
        movie = self._session.query(Movie).filter_by(id=id).first()
        return movie