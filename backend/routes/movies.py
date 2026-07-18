"""Routes for browsing, searching, and importing movies."""

from fastapi import APIRouter, Query, Depends, status
from typing import List
import httpx
import logging

from sqlalchemy.orm import Session

from models.movie import MoviesResponse, TMDBResponse
from services.movie_service import MovieService

from db.database import get_db

from utility.utils import get_env_key

logger = logging.getLogger(__name__)

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w220_and_h330_face"

TMDB_API_KEY = get_env_key("TMDB_API_KEY")


def add_poster_url(movie: TMDBResponse) -> TMDBResponse:
    """Rewrite a TMDB-relative poster path into a full, displayable image URL."""
    movie
    if movie.poster_path is None:
        return movie
    else:
        movie.poster_path = f"{POSTER_BASE_URL}/{movie.poster_path}"
        return movie


async def fetch_latest_popular_movies(page: int = 1) -> List[TMDBResponse]:
    """Fetch one page of "popular movies" results from the TMDB API."""
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": TMDB_API_KEY, "page": page}
    movies: List[TMDBResponse] = []

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            fetched_movies: List = response.json()["results"]
            movies = [add_poster_url(TMDBResponse(**movie)) for movie in fetched_movies]

        except httpx.RequestError as e:
            raise logger.error(f"HTTP Request Error: {e}")

        except Exception as e:
            logger.error(f"Error fetching latest popluar movies : {e}")

    return movies


@router.get("/load_movies", response_model=MoviesResponse)
async def load_movies(
    pages: int = Query(15, ge=1), session: Session = Depends(get_db)
) -> MoviesResponse:
    """
    Fetch popular movies from TMDB server and load them into database.
    """
    logger.debug(f"load popular movies endpoint invoked with pages={pages}")
    movie_service = MovieService(session)
    for page in range(1, pages + 1):
        popular_movies = await fetch_latest_popular_movies(page)
        movie_service.add_movies(popular_movies)

    return MoviesResponse(movies=movie_service.get_movies_by_page(1))


@router.get("/movies", response_model=MoviesResponse)
async def movies_by_page(
    page: int = Query(1, ge=1), session: Session = Depends(get_db)
) -> MoviesResponse:
    """Return one page of movies already stored in the database."""
    logger.debug(f"Movies requested for page {page}")
    movie_service = MovieService(session)
    movies = movie_service.get_movies_by_page(page)
    return MoviesResponse(movies=movies)


@router.get("/search", response_model=MoviesResponse)
async def search_movie(
    query: str = Query(...), session: Session = Depends(get_db)
) -> MoviesResponse:
    """Search movies by free-text query.

    NOTE: MovieService currently has no `search_movies` method (only
    `similarity_search`, which needs an embedding rather than raw text), so
    this route will raise an AttributeError at runtime. Left as-is per
    request - not fixed here.
    """
    logger.debug(f"Search movies endpoint invoked with query: {query}")

    movie_service = MovieService(session)
    movies = movie_service.search_movies(query)
    return movies
