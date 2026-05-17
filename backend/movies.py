from fastapi import APIRouter, Query
from typing import List
from dotenv import load_dotenv, find_dotenv, get_key
import httpx
from urllib.parse import quote
import time
import logging
from models.movies import Movie, Movies, IsLoaded

logger = logging.getLogger(__name__)

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL  ="https://image.tmdb.org/t/p/w220_and_h330_face"

env_path = find_dotenv()
load_dotenv(env_path, override=True)
API_KEY = get_key(env_path, "TMDB_API_KEY")

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

async def fetch_popular_movies_seeds() -> Movies:
    all_movies: List[Movie] = []
    url = f"{BASE_URL}/movie/popular"
    client = httpx.AsyncClient()
    for page in range(1, 501):
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
    
    return Movies(movies=all_movies)




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

@router.get("/load_seeds", response_model=IsLoaded)
async def load_popular_movies_seeds() -> IsLoaded:
    logger.info("Load seeds endpoint invoked")
    try:
        seeds = await fetch_popular_movies_seeds()
        logger.info("Seeds loaded successfully")
        return IsLoaded(is_loaded=True)
    except Exception as e:
        logger.error(f"Error loading seeds: {e}")
        return IsLoaded(is_loaded=False)