from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage

from sqlalchemy.orm import Session

from services.movie_service import MovieService
from services.user_service import UserService
from ai.llm import get_llm_model, get_embedding_model

from models.ask_ai import QueryResponse
from models.movie import MovieResponse

from logging import getLogger
logger = getLogger(__name__)

from typing import List


class MovieRAGAgent:
    """
    Intelligent agent for movie suggestions using RAG and pgvector.
    
    Features:
    - Retrieves user's liked movies from database
    - Extracts genres from user query
    - Performs similarity search on combined genre embeddings
    - Returns JSON formatted suggestions
    """

    __GENRE_ID_MAP = {
        "action": 28, "adventure": 12, "animation": 16, "comedy": 35,
        "crime": 80, "documentary": 99, "drama": 18, "family": 10751,
        "fantasy": 14, "history": 36, "horror": 27, "music": 10402,
        "mystery": 9648, "romance": 10749, "sci-fi": 878,
        "thriller": 53, "war": 10752, "western": 37,
    }

    __SYSTEM_MESSAGE = SystemMessage(content="""You are an intelligent movie recommendation agent.
                                         
Your workflow steps are as follows:
1. First, retrieve the user's liked movies genre ids to understand user's preferences
2. Extract genre preferences from the user's search query
3. Search for similar movies using the combined genre (from step 1 and step 2) and similarity search
4. Provide personalized movie recommendations based on the similarity search results

Always be helpful, friendly, and provide reasoning for your recommendations.
Format your final answer with movie titles, genres, and brief descriptions.""")

    def __init__(self, session: Session):
        self.__movie_service = MovieService(session)
        self.__user_service = UserService(session)
        self.__llm = get_llm_model()
        tools = [self.__get_user_liked_movies_genre_ids, self.__extract_genres_from_query, self.__perform_similarity_search]

        self.__agent = create_agent(llm=self.__llm, tools=tools, system_prompt=self.__SYSTEM_MESSAGE)

    
    @tool
    def __get_user_liked_movies_genre_ids(self, user_id: str) -> List[int]:
        """
        Retrieve all movies genre ids liked by a specific user.
        
        Args:
            user_id: UUID of the user
            
        Returns:
            List of user's liked movies genre ids
        """
        user = self.__user_service.get_user_by_id(user_id)
        movies = [self.__movie_service.get_movie_by_id(movie_id) for movie_id in user.favorite_movies]
        all_genres: List[int] = []
        for movie in movies:
            all_genres = [*all_genres, *movie.genre_ids]
        return list(set(all_genres))
    
    @tool
    def __extract_genres_from_query(self, query: str) -> List[int]:
        """
        Extract genre ids from user query using LLM.
        
        Args:
            query: User's search query
            
        Returns:
            List of extracted genre ids
        """
        try:
            
            extraction_prompt = f"""
            Extract genre ids from the following movie search query.
            Return a list of genre ids. Only return valid movie genres.
            
            Query: {query}
            
            Example genres: action, comedy, crime, drama, documentary, family, horror, sci-fi, music, history, romance, thriller, mystery, adventure, animation, fantasy, western, war
            
            Return only the list from exaample genres, no other text.
            """
            
            response = self.__llm.invoke([HumanMessage(content=extraction_prompt)])
            genres_str = response.content.strip()
            logger.info(f"Extracted genre: {genres_str}")
            # TODO: map string genres to ids via self.__GENRE_ID_MAP
            return genres_str
        except Exception as e:
            logger.error("Error extracting genres from query.")
            return []
        

    @tool
    def __perform_similarity_search(
        self,
        genres: List[int],
    ) -> List[MovieResponse]:
        """
        Perform similarity search on movies combining genre filters and embeddings.
        
        Args:
            query_text: Original user query for embedding
            genres: List of genre filters
            limit: Number of results to return
            
        Returns:
            List of suggested movies with similarity scores
        """
        try:
            query_embedding = get_embedding_model(True).embed_query(str(genres))
            movies = self.__movie_service.similarity_search(query_embedding)
            return movies
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []
    
    
    def suggest_movies(
        self,
        query: str
    ) -> QueryResponse:
        """
        Main method to get movie suggestions for a user.
        
        Args:
            user_id: UUID of the user
            query: User's search query
            limit: Number of movies suggestions
        Returns:
            QueryResponse with AI answer and data
        """
        
        user_id = self.__user_service.get_user().id
        
        try:
            # Execute agent
            response = self.__agent.invoke({"input": f"""Please suggest movies for this user (UUID: {user_id}) based on user's query: "{query}"."""})
            
            ai_answer = response.get("output", "No recommendations generated")
            
            return QueryResponse(
                answer=ai_answer,
                movies=[]
            )
        
        except Exception as e:
            logger.error(f"Error generating agent reponse due to {e}")
            return QueryResponse(
                answer=f"Error generating movies suggestions.",
                movies=[]
            )

