from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from uuid import UUID
from sqlalchemy.orm import Session
import json

from services.movie_service import MovieService

from ai.llm import get_llm_model, get_embedding_model

from models.ask_ai import QueryResponse
from models.movie import MovieResponse

from typing import List, TypedDict, Tuple, Any

from logging import getLogger

logger = getLogger(__name__)


class MovieRAGAgent:
    """
    Intelligent agent for movie suggestions utilizing Agents and RAG.

    Features:
    - Extracts genres from user query
    - Performs similarity search on LLM extracted genres to embeddings
    - Returns JSON formatted suggestions
    """

    __SYSTEM_MESSAGE = SystemMessage(content="""You are a movie recommendation agent.

CORE RULE: Call the tool search_similar_movies if, and only if, the query is a request for movie suggestions. Do not call it for anything else. Never call it more than once per query. Never answer movie suggestions from your own knowledge — always rely on the tool's results.

Valid genres: action, comedy, crime, drama, documentary, family, horror, science-fiction, music, history, romance, thriller, mystery, adventure, animation, fantasy, western, war

TOOL:
- search_similar_movies(genres_text): Call ONLY when the query is asking for movie suggestions/recommendations. genres_text is a comma-separated string of genres.

STEPS:
1. Determine whether the query is a movie-suggestion request.
   - If NOT a movie-suggestion request: do NOT call any tool. Go directly to the output format below, with an answer stating you can only help with movie suggestions, and an empty ids list.
   - If it IS a movie-suggestion request: continue to step 2.
2. Extract valid genres explicitly mentioned in the query. If none are explicit, infer the closest matching genre(s) from the query's meaning.
3. Call search_similar_movies exactly once, passing the genres as a comma-separated string.
4. Use the returned movie overviews to write a short, friendly summary, and collect all returned movie ids.
5. Output ONLY valid JSON, nothing else — no explanation, no markdown, no code fences:
{"answer": "<friendly reasoning summary>", "ids": [<movie ids>]}""")

    def __init__(self, session: Session):
        self.__movie_service = MovieService(session)
        self.__llm = get_llm_model()
        tools = self.__get_agent_tools()
        self.__agent = create_agent(
            model=self.__llm, tools=tools, system_prompt=self.__SYSTEM_MESSAGE
        )

    def __get_agent_tools(self):
        class SimilarMovies(TypedDict):
            id: str
            title: str
            overview: str

        @tool
        def search_similar_movies(
            genres_text: str,
        ) -> List[SimilarMovies]:
            """
            Searches similar movies using genres text provided as parameter.

            Args:
                genres_text: comma-separated genres text

            Returns:
                List of movie ids
            """
            logger.debug(
                f"Agent: Performing similarity search on Genres: {genres_text}."
            )
            try:
                query_embedding = get_embedding_model().embed_query(genres_text)
                movies = self.__movie_service.similarity_search(query_embedding)
                return [
                    SimilarMovies(
                        id=str(movie.id),
                        title=movie.title,
                        overview=movie.overview,
                    )
                    for movie in movies
                ]
            except Exception as e:
                logger.error(f"Error performing similarity search: {str(e)}")
                return []

        return [search_similar_movies]

    def suggest_movies(self, query: str) -> Tuple[str, List[MovieResponse]]:
        """
        Main method to get movie suggestions for a user.

        Args:
            query: User's search query
        Returns:
            Tuple with AI answer and suggested movies
        """

        try:
            response = self.__agent.invoke(
                {"messages": [HumanMessage(f"Query: {query}")]}
            )

            ai_answer = response.get("messages")[-1].content

            logger.debug(f"AI Message: {ai_answer}")

            if isinstance(ai_answer, str):
                ai_answer = json.loads(ai_answer)

            if isinstance(ai_answer, list):
                ai_answer = ai_answer[-1].get("text")
                if isinstance(ai_answer, str):
                    ai_answer = json.loads(ai_answer)

            answer = ai_answer.get("answer")
            ids: List[str] = ai_answer.get("ids", [])

            movies: List[MovieResponse] = []

            for id in ids:
                try:
                    movie = self.__movie_service.get_movie_by_id(UUID(id))
                    movies.append(movie)
                except Exception as e:
                    logger.error(
                        f"Could not fetch movie with id: {id} deu to {e}. Skipping..."
                    )

            return (answer, movies)

        except Exception as e:
            logger.error(f"Error generating agent reponse due to {e}")
            return QueryResponse(
                answer=f"Error generating movies suggestions.", movies=[]
            )
