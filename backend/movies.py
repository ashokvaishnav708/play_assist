from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv, find_dotenv, get_key
import httpx
from urllib.parse import quote

router = APIRouter()

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL  ="https://image.tmdb.org/t/p/w220_and_h330_face"

env_path = find_dotenv()
load_dotenv(env_path, override=True)
API_KEY = get_key(env_path, "TMDB_API_KEY")

class Movie(BaseModel):
    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str

class Movies(BaseModel):
    movies: List[Movie]


async def fetch_movies(url: str) -> List[Movies]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        fetched_movies: List = response.json()["results"]
        movies = [Movie(**(movie | { "poster_path": f"{POSTER_BASE_URL}/{movie["poster_path"]}" if movie["poster_path"] else None}) ) for movie in fetched_movies]
        return movies

@router.get("/popular", response_model=Movies)
async def popular_movies() -> Movies:
    popular_movies_url = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    popular_movies = await fetch_movies(popular_movies_url)
    return Movies(movies=popular_movies)

@router.get("/search", response_model=Movies)
async def search_movie(query: str) -> Movies:
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={quote(query)}"
    search_result = await fetch_movies(search_url)
    return Movies(movies=search_result)