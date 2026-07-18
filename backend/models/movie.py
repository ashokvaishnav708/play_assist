"""Pydantic request/response models for movie data, distinct from the
SQLAlchemy ORM model in db/schema.py."""

from typing import List
from pydantic import BaseModel
from uuid import UUID


class TMDBResponse(BaseModel):
    """Shape of a single movie result as returned by the TMDB API."""

    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_ids: List[int]


class MovieCreateRequest(BaseModel):
    """Fields needed to persist a movie, after mapping TMDB genre ids to names."""

    tmdb_id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_types: List[str]


class MovieResponse(BaseModel):
    """Movie as returned to API clients, including its internal id."""

    id: UUID
    tmdb_id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_types: List[str]


class MoviesPageRequest(BaseModel):
    """Pagination request for GET /movies/movies."""

    page: int


class LoadMoviesRequest(BaseModel):
    """Request to bulk-import a number of pages of movies from TMDB."""

    pages: int


class MoviesResponse(BaseModel):
    """A list of movies, used by list/search/page endpoints."""

    movies: List[MovieResponse]
