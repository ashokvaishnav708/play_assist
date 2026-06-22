from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv, get_key

from models.movie import MovieCreateRequest as Movie
from agent.movies import movie_store

from logging import getLogger
logger = getLogger(__name__)

from typing import List

def get_movies_via_genre(genre_ids: List[int]) -> List[Movie]:
    """
    Gets all the movies matching genre ids.

    @param genre_ids: List of genre ids
    @return: List of movies ids
    """
    movies = movie_store.get_movies()

    search_set = set(genre_ids)
    movies_id = [movie.id for movie in movies if not search_set.isdisjoint(movie.genre_ids)]

    return movies_id



SYSTEM_MESSAGE = SystemMessage(content="""You are a helpful assistant for movies suggestions.
                               Tools: {get_movies_via_genre}
                               The genre and associated genre ids for movies are Action = 28, Adventure = 12, Animation = 16, Comedy = 35, Crime = 80, Documentary = 99, Drama = 18, Family = 10751, Fantasy = 14, History = 36, Horror = 27, Music = 10402, Mystery = 9648, Romance = 10749, Science Fiction (Sci-Fi) = 878, Thriller = 53, War = 10752, Western = 37.
                               If user queries for movie suggestions, get movie genre idea from query, collect genre ids and get movies via genre.
                               Observation: If list is empty the print: empty list, for eg: []. Else, print all the movies ids in the list format like [id1, id2, ...].
                               """)

class MovieAgent:
    def __init__(self, gemini_api_key: str):
        self.__llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=gemini_api_key, temperature=0.3)
        self.__agent = create_agent(
            model=self.__llm,
            tools=[get_movies_via_genre],
            system_prompt=SYSTEM_MESSAGE)
        
    def query_agent(self, query: str):
        result = self.__agent.invoke({
            "messages": [HumanMessage(content=query)]
        })

        logger.debug(f"Agent resposnse: {result['messages'][-1].content_blocks}")
        logger.info(f"Messages {result['messages']}")
        # Sample response from agent 
        # [{'type': 'text', 'text': 'OK. Here are some action movies for you: [id1, id2, ...., id_n ].'}]
        


env_path = find_dotenv()
load_dotenv(env_path, override=True)
GOOGLE_API_KEY = get_key(env_path, "GEMINI_API_KEY")

movie_agent = MovieAgent(gemini_api_key=GOOGLE_API_KEY)

