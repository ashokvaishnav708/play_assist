from fastapi import APIRouter
from logging import getLogger

from models.ask_ai import QueryRequest, QueryResponse
from rag.rag_chain import rag_chain
from agent.agent import movie_agent

logger = getLogger(__name__)

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_ai(request: QueryRequest) -> QueryResponse:
    query = request.question
    logger.info(f"AI query received: {query}")
    
    answer, movies = rag_chain.query(query)
    return QueryResponse(answer=answer, movies=movies)

@router.post("/query_agent", response_model=QueryResponse)
async def query_agent(request: QueryRequest) -> QueryResponse:
    query = request.question
    logger.debug(f"Agent query received: {query}")
    movie_agent.query_agent(query)

    return QueryResponse(answer="", movies=[])



