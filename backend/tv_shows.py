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

class TVShow(BaseModel):
    id: int
    title: str
    release_date: str
    poster_path: str | None
    original_language: str
    overview: str

class TVShows(BaseModel):
    tv_shows: List[TVShow]


async def fetch_tv_shows(url: str) -> List[TVShows]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        fetched_tv_shows: List = response.json()["results"]
        tv_shows = [TVShow(**tv_show) for tv_show in fetched_tv_shows]
        return tv_shows

@router.get("/popular", response_model=TVShows)
async def popular_tv_shows() -> TVShows:
    popular_tv_shows_url = f"{BASE_URL}/tv/popular?api_key={API_KEY}"
    popular_tv_shows = await fetch_tv_shows(popular_tv_shows_url)
    return TVShows(tv_shows=popular_tv_shows)

@router.get("/search", response_model=TVShows)
async def search_tv_show(query: str) -> TVShows:
    search_url = f"{BASE_URL}/search/tv?api_key={API_KEY}&query={quote(query)}"
    search_result = await fetch_tv_shows(search_url)
    return TVShows(tv_shows=search_result)