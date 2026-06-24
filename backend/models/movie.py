from typing import List
from pydantic import BaseModel

class MovieCreateRequest(BaseModel):
    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_ids: List[int]

class MovieResponse(BaseModel):
    id: str
    tmdb_id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_ids: List[int]

class MoviesPageRequest(BaseModel):
    page: int

class LoadMoviesRequest(BaseModel):
    pages: int


class MoviesResponse(BaseModel):
    movies: List[MovieResponse]
