from typing import List
from pydantic import BaseModel
from uuid import UUID


class TMDBResponse(BaseModel):
    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_ids: List[int]


class MovieCreateRequest(BaseModel):
    tmdb_id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_types: List[str]


class MovieResponse(BaseModel):
    id: UUID
    tmdb_id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_types: List[str]


class MoviesPageRequest(BaseModel):
    page: int


class LoadMoviesRequest(BaseModel):
    pages: int


class MoviesResponse(BaseModel):
    movies: List[MovieResponse]
