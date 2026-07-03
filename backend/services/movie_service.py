from db.respository.movie import MovieRepository
from models.movie import MovieCreateRequest, MovieResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ai.llm import get_embedding_model

from typing import List

import logging
logger = logging.getLogger(__name__)

MOVIES_PER_PAGE = 40

class MovieService:
    def __init__(self, session: Session):
        self.__movie_repo = MovieRepository(session=session)
        self.__embedding_model = get_embedding_model()

    def movie_to_text(self, movie: MovieCreateRequest) -> str:
        return f"""
        Title: {movie.title}
        Overview: {movie.overview}
        Release Date: {movie.release_date}
        Original Language: {movie.original_language}
        Genre: {movie.genre_ids}
        """.strip()

    def add_movie(self, movie: MovieCreateRequest) -> MovieResponse:
        if self.__movie_repo.get_movie_by_tmdb_id(movie.tmdb_id):
            raise HTTPException(status_code=400, detail="Movie already exists. Skipping...")

        movie_text = self.movie_to_text(movie)
        embedding = self.__embedding_model.embed_query(movie_text)

        movie = self.__movie_repo.create_movie(movie, embedding)

        return MovieResponse(**movie.__dict__)
    
    def add_movies(self, movies: List[MovieCreateRequest]):
        for movie in movies:
            try:
                self.add_movie(movie)
            except Exception as e:
                logger.error(f"{e}")

    
    def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        movie = self.__movie_repo.get_movie_by_id(id=movie_id)

        if movie:
            return MovieResponse(**movie.__dict__)
        raise HTTPException(status_code=400, detail=f"Movie is not avaialbale with {movie_id}.")
    
    def get_movies_by_page(self, page: int) -> List[MovieResponse]:
        offset = (page - 1) * MOVIES_PER_PAGE
        limit = MOVIES_PER_PAGE

        movies = self.__movie_repo.get_movies_by_range(offset=offset, limit=limit)
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response
    
    def search_movies(self, keyword: str) -> List[MovieResponse]:
        movies = self.__movie_repo.search_movie_by_keyword(keyword=keyword)
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response
    
    def similarity_search(self, query_embeddings: List[float]) -> List[MovieResponse]:
        movies = self.__movie_repo.similarity_search(query_embeddings)
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response
    
    def get_all_movies(self) ->List[MovieResponse]:
        movies = self.__movie_repo.get_all_movies()
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response
