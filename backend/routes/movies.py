from fastapi import APIRouter, Query
from typing import List
import httpx
from urllib.parse import quote
import time
import logging

from models.movies import Movie, Movies

from db.models import Movie as DBMovie
from db.database import get_db

from backend.utility.utils import get_env_key

logger = logging.getLogger(__name__)

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL  ="https://image.tmdb.org/t/p/w220_and_h330_face"

API_KEY = get_env_key("TMDB_API_KEY")

def add_poster_url(movie: Movie) -> Movie:
    if movie.poster_path is None:
        return movie
    else:
        movie.poster_path = f'{POSTER_BASE_URL}/{movie.poster_path}'
        return movie
    
async def fetch_movies(url: str) -> List[Movies]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        fetched_movies: List = response.json()["results"]
        movies = [add_poster_url(Movie(**movie)) for movie in fetched_movies]
        return movies

async def fetch_popular_movies_seeds() -> List[Movies]:
    all_movies: List[Movie] = []
    url = f"{BASE_URL}/movie/popular"
    client = httpx.AsyncClient()
    for page in range(1, 10):
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": page
        }

        try: 
            resposne = await client.get(url, params=params)

            if resposne.status_code == 200:
                data = resposne.json()
                fetched_movies = data["results"]
                movies = [add_poster_url(Movie(**movie)) for movie in fetched_movies]
                all_movies.extend(movies)
            elif resposne.status_code == 429:
                # Too many requests need to wait
                retry_after = int(resposne.headers.get("Retry-After", 2))
                logger.warning(f"Rate limit hit on page {page}. Sleeping for {retry_after} seconds...")
                time.sleep(retry_after)

                page -= 1
                continue
            else:
                logger.error(f"Failed on page {page} with status code {resposne.status_code}")
                break
    
        except httpx.RequestError as e:
            logger.error(f"Error fetching seeds due to {e}")
            break
    
    return all_movies

def add_movies_to_db(movies: List[Movie]):
    with get_db() as db:
        for movie in movies:
            db_movie = DBMovie(
                tmdb_id=movie.id, 
                title=movie.title,
                release_date=movie.release_date,
                poster_path=movie.poster_path,
                original_language=movie.original_language,
                overview=movie.overview,
                genre_ids=movie.genre_ids
                )
            db.add(db_movie)
            db.commit()
            db.refresh(db_movie)


@router.get("/popular", response_model=Movies)
async def popular_movies() -> Movies:
    logger.info("Popular movies endpoint invoked")
    popular_movies_url = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    popular_movies = await fetch_movies(popular_movies_url)
    return Movies(movies=popular_movies)

@router.get("/search", response_model=Movies)
async def search_movie(query: str = Query(...)) -> Movies:
    logger.info(f"Search movies endpoint invoked with query: {query}")
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={quote(query)}"
    search_result = await fetch_movies(search_url)
    return Movies(movies=search_result)
