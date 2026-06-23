from db.respository.movie import MovieRepository
from models.movie import MovieCreateRequest as Movie
from fastapi import HTTPException
from sqlalchemy.orm import Session

from typing import List


class MovieService:
    def __int__(self, session: Session):
        self.__movie_repo = MovieRepository(session=session)

    def add_movie(self, movie_data: Movie) -> Movie:
        if self.__movie_repo.get_movie_by_tmdb_id(movie_data.tmdb_id):
            raise HTTPException(status_code=400, detail="Movie already exists. Skipping...")

        movie = self.__movie_repo.create_movie(movie_data=movie_data)

        return Movie(**movie)
    
    def add_movies(self, movies: List[Movie]):
        for movie in movies:
            self.add_movie(movie)
    
    def get_movie_by_id(self, movie_id: int) -> Movie:
        movie = self.__movie_repo.get_movie_by_id(id=movie_id)

        if movie:
            return Movie(**movie)
        raise HTTPException(status_code=400, detail=f"Movie is not avaialbale with {movie_id}.")
    
    def get_movies_by_page(self, page: int) -> List[Movie]:
        movies = self.__movie_repo.get_movies_by_page(page)
        return movies
    
    def search_movies(self, keyword: str) -> List[Movie]:
        movies = self.__movie_repo.search_movie_by_keyword(keyword=keyword)
        return movies