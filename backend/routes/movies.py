from fastapi import APIRouter, Query, Depends, status
from typing import List
import httpx
import logging

from sqlalchemy.orm import Session

from models.movie import MovieCreateRequest, MoviesResponse, MoviesPageRequest, LoadMoviesRequest
from services.movie_service import MovieService

from db.database import get_db

from utility.utils import get_env_key

logger = logging.getLogger(__name__)

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL  ="https://image.tmdb.org/t/p/w220_and_h330_face"

TMDB_API_KEY = get_env_key("TMDB_API_KEY")
MOVIES_LANGUAGE = get_env_key("MOVIES_LANGUAGE")

def add_poster_url(movie: MovieCreateRequest) -> MovieCreateRequest:
    if movie.poster_path is None:
        return movie
    else:
        movie.poster_path = f'{POSTER_BASE_URL}/{movie.poster_path}'
        return movie

    
async def fetch_latest_popular_movies(page: int = 1) -> List[MovieCreateRequest]:
    url = f"{BASE_URL}/movie/popular"
    params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US" if MOVIES_LANGUAGE is None else MOVIES_LANGUAGE,
            "page": page
        }
    movies: List[MovieCreateRequest] = []

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            fetched_movies: List = response.json()["results"]
            movies = [add_poster_url(MovieCreateRequest(**movie)) for movie in fetched_movies]

        except httpx.RequestError as e:
            raise logger.error(f"HTTP Request Error: {e}")

        except Exception as e:
            logger.error(f"Error fetching latest popluar movies : {e}")

    return movies


@router.get("/load_movies", status_code=status.HTTP_200_OK)
async def load_movies(request_body: LoadMoviesRequest, session: Session = Depends(get_db)) -> MoviesResponse:
    """
    Fetch popular movies from TMDB server and load them into database.
    """
    logger.debug("load popular movies endpoint invoked")
    movie_service = MovieService(session)
    for page in range(request_body.pages):
        popular_movies = await fetch_latest_popular_movies(page)
        movie_service.add_movies(popular_movies)


@router.get("/movies", response_model=MoviesResponse)
async def movies_by_page(request_body: MoviesPageRequest, session: Session = Depends(get_db)) -> MoviesResponse:
    page = request_body.page
    logger.debug(f"Movies requested for page {page}")

    movie_service = MovieService(session)
    movies = movie_service.get_movies_by_page(page)

    return MoviesResponse(movies=movies)

@router.get("/search", response_model=MoviesResponse)
async def search_movie(query: str = Query(...), session: Session = Depends(get_db)) -> MoviesResponse:
    logger.debug(f"Search movies endpoint invoked with query: {query}")
    
    movie_service = MovieService(session)
    movies = movie_service.search_movies(query)
    return movies
    
