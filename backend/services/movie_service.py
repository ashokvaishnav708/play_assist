from db.respository.movie import MovieRepository
from models.movie import MovieCreateRequest, MovieResponse, TMDBResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ai.llm import get_embedding_model

from typing import List

import logging

logger = logging.getLogger(__name__)

MOVIES_PER_PAGE = 40


class MovieService:
    __GENRE_ID_TO_TYPE_MAP = {
        28: "action",
        12: "adventure",
        16: "animation",
        35: "comedy",
        80: "crime",
        99: "documentary",
        18: "drama",
        10751: "family",
        14: "fantasy",
        26: "history",
        27: "horror",
        10402: "music",
        9648: "mystery",
        10749: "romance",
        878: "science-fiction",
        10770: "tv-movie",
        53: "thriller",
        10752: "war",
        37: "western",
    }

    def __init__(self, session: Session):
        self.__movie_repo = MovieRepository(session=session)
        self.__embedding_model = get_embedding_model()

    def __get_genre_types_to_text(self, genre_types: List[str]) -> str:
        return ", ".join(genre_types)

    def __movie_to_text(self, movie: MovieCreateRequest) -> str:
        return f"""
        Title: {movie.title}
        Overview: {movie.overview}
        Release Date: {movie.release_date}
        Original Language: {movie.original_language}
        Genre: {self.__get_genre_types_to_text(movie.genre_types)}
        """.strip()

    def __get_genre_ids_to_type(self, genre_ids: List[int]) -> List[str]:
        genre_types: List[str] = []
        for id in genre_ids:
            genre_type = self.__GENRE_ID_TO_TYPE_MAP.get(id)
            if genre_type != None:
                genre_types.append(genre_type)

        return genre_types

    def __generate_embedding(self, text: str) -> List[float]:
        try:
            embedding = self.__embedding_model.embed_query(text)
            return embedding
        except Exception as e:
            logger.log(f"Error generating embedding due to {e}.")
            return []

    def add_movie(self, movie: TMDBResponse) -> MovieResponse:
        ### movie.id refers to TMDB movie id
        if self.__movie_repo.get_movie_by_tmdb_id(movie.id):
            raise HTTPException(
                status_code=400, detail="Movie already exists. Skipping..."
            )

        genre_types = self.__get_genre_ids_to_type(movie.genre_ids)

        ### Parse TMDB response to movie create request model type
        movie_to_create = MovieCreateRequest(
            **movie.model_dump(), tmdb_id=movie.id, genre_types=genre_types
        )

        movie_text = self.__movie_to_text(movie_to_create)

        embedding = self.__embedding_model.embed_query(movie_text)
        logger.info(f"Embedding lenght: {len(embedding)}")
        movie = self.__movie_repo.create_movie(movie_to_create, embedding)

        return MovieResponse(**movie.__dict__)

    def add_movies(self, movies: List[TMDBResponse]):
        for movie in movies:
            try:
                self.add_movie(movie)
            except Exception as e:
                logger.error(f"{e}")

    def get_movie_by_id(self, movie_id: UUID) -> MovieResponse:
        movie = self.__movie_repo.get_movie_by_id(id=movie_id)

        if movie:
            return MovieResponse(**movie.__dict__)
        raise HTTPException(
            status_code=400, detail=f"Movie is not avaialbale with {movie_id}."
        )

    def get_movies_by_page(self, page: int) -> List[MovieResponse]:
        offset = (page - 1) * MOVIES_PER_PAGE
        limit = MOVIES_PER_PAGE

        movies = self.__movie_repo.get_movies_by_range(offset=offset, limit=limit)
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response

    def similarity_search(self, query_embeddings: List[float]) -> List[MovieResponse]:
        movies = self.__movie_repo.similarity_search(query_embeddings)
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response

    def get_all_movies(self) -> List[MovieResponse]:
        movies = self.__movie_repo.get_all_movies()
        movies_response = [MovieResponse(**movie.__dict__) for movie in movies]
        return movies_response
