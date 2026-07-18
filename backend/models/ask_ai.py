"""Pydantic request/response models for the /ask_ai endpoint."""

from typing import List
from pydantic import BaseModel

from models.movie import MovieResponse


class QueryRequest(BaseModel):
    """Body of a POST /ask_ai/query request."""

    question: str


class QueryResponse(BaseModel):
    """AI-generated answer plus the movies it recommends."""

    answer: str
    movies: List[MovieResponse]
