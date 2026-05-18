from typing import List
from pydantic import BaseModel

from models.movies import Movie

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    movies: List[Movie] 