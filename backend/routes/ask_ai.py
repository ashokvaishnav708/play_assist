from fastapi import APIRouter
from logging import getLogger

from models.ask_ai import QueryRequest, QueryResponse
from rag.rag_chain import rag_chain

logger = getLogger(__name__)

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_ai(request: QueryRequest) -> QueryResponse:
    query = request.question
    logger.info(f"AI query received: {query}")
    
    answer, movies = rag_chain.query(query)
    return QueryResponse(answer=answer, movies=movies)