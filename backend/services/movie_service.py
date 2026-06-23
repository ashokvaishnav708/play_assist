from db.respository.movie import MovieRepository
from models.movie import MovieCreateRequest as Movie
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ai.llm import get_embedding_model

from typing import List


class MovieService:
    def __int__(self, session: Session):
        self.__movie_repo = MovieRepository(session=session)
        self.__embedding_model = get_embedding_model()

    def add_movie(self, movie: Movie) -> Movie:
        if self.__movie_repo.get_movie_by_tmdb_id(movie.tmdb_id):
            raise HTTPException(status_code=400, detail="Movie already exists. Skipping...")

        movie_text = f"""
        Title: {movie.title}
        Poster: {movie.poster_path}
        Overview: {movie.overview}
        Release Date: {movie.release_date}
        Original Language: {movie.original_language}
        Genre: {movie.genre_ids}
        """.strip()
        embedding = self.__embedding_model.embed_query(movie_text)

        movie = self.__movie_repo.create_movie(movie, embedding)

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