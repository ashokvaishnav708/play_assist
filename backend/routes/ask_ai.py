from fastapi import APIRouter, Depends
from logging import getLogger

from models.ask_ai import QueryRequest, QueryResponse

from db.database import get_db
from sqlalchemy.orm import Session

from ai.movie_rag_agent import MovieRAGAgent
from services.user_service import UserService

logger = getLogger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_ai(
    request: QueryRequest, session: Session = Depends(get_db)
) -> QueryResponse:
    query = request.question
    logger.debug(f"AI query received: {query}")

    agent = MovieRAGAgent(session)

    answer, movies = agent.suggest_movies(query)

    logger.debug(f"Answer: {answer}")
    logger.debug(f"Movies length: {len(movies)}")

    return QueryResponse(answer=answer, movies=movies)
