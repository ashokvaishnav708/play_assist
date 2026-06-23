from fastapi import APIRouter, Query, Depends
from typing import List
import httpx
import time
import logging

from sqlalchemy.orm import Session

from models.movie import MovieCreateRequest as Movie, MoviesResponse as Movies, MoviesPageRequest, LoadMoviesRequest
from services.movie_service import MovieService

from db.schema import Movie as DBMovie
from db.database import get_db

from utility.utils import get_env_key

logger = logging.getLogger(__name__)

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL  ="https://image.tmdb.org/t/p/w220_and_h330_face"

API_KEY = get_env_key("TMDB_API_KEY")
MOVIES_LANGUAGE = get_env_key("MOVIES_LANGUAGE")

def add_poster_url(movie: Movie) -> Movie:
    if movie.poster_path is None:
        return movie
    else:
        movie.poster_path = f'{POSTER_BASE_URL}/{movie.poster_path}'
        return movie
    
async def fetch_movies(url: str, params: dict = {}) -> List[Movies]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            fetched_movies: List = response.json()["results"]
            movies = [add_poster_url(Movie(**movie)) for movie in fetched_movies]
            return movies
        except httpx.RequestError as e:
            raise httpx.RequestError(f"HTTP Request Error: {e}")

    
async def fetch_latest_popular_movies(page: int = 1) -> List[Movie]:
    url = f"{BASE_URL}/movie/popular"
    params = {
            "api_key": API_KEY,
            "language": "en-US" if MOVIES_LANGUAGE is None else MOVIES_LANGUAGE,
            "page": page
        }
    movies: List[Movie] = []

    try:
        movies = fetch_movies(url, params)

    except Exception as e:
        logger.error(f"Error fetching latest popluar movies : {e}")

    return movies


@router.get("/load_movies", response_model=Movies)
async def load_movies(request: LoadMoviesRequest, session: Session = Depends(get_db)) -> Movies:
    """
    Fetch popular movies from TMDB server and load them into database.
    """
    logger.debug("load popular movies endpoint invoked")
    movie_service = MovieService(session)
    for page in range(request.pages):
        popular_movies = await fetch_latest_popular_movies(page)

    movie_service.add_movies(popular_movies)

    return Movies(movies=popular_movies)


@router.get("/movies", response_model=Movies)
async def movies_by_page(query: MoviesPageRequest, session: Session = Depends(get_db)) -> Movies:
    page = query.page
    logger.debug(f"Movies requested for page {page}")

    movie_service = MovieService(session)
    movies = movie_service.get_movies_by_page(page)

    return Movies(movies=movies)

@router.get("/search", response_model=Movies)
async def search_movie(query: str = Query(...), session: Session = Depends(get_db)) -> Movies:
    logger.debug(f"Search movies endpoint invoked with query: {query}")
    
    movie_service = MovieService(session)
    movies = movie_service.search_movies(query)
    return movies
    
