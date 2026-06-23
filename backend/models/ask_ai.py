from typing import List
from pydantic import BaseModel

from models.movie import MovieCreateRequest

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    movies: List[MovieCreateRequest] 