from typing import List
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str
    genre_ids: List[int]

class Movies(BaseModel):
    movies: List[Movie]
