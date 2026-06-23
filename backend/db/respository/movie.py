from .base import BaseRepository
from db.schema import Movie
from models.movie import MovieCreateRequest

from typing import List


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
    
    def get_movie_by_tmdb_id(self, tmdb_id: str) -> List[Movie]:
        movies = self._session.query(Movie).filter_by(tmdb_id=tmdb_id).all()
        return movies
    
    def get_movie_by_id(self, id: int) -> Movie | None:
        movie = self._session.query(Movie).filter_by(id=id).first()
        return movie
    
    def get_movies_by_page(self, page: int) -> List[Movie]:
        movies = self._session.query(Movie).filter_by(page=page).all()
        return movies
    
    def search_movie_by_keyword(self, keyword: str) -> List[Movie]:
        movies = self._session.query(Movie).filter(Movie.title.ilike(f'%{keyword}%')).all()
        return movies