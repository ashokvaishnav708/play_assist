import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes.movies import router as movies_router
from routes.ask_ai import router as ask_ai
from routes.auth import router as auth_router

# from routes.tv_shows import router as tv_shows_router

from db.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
# Suppress logs from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


DEBUG = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(debug=DEBUG, lifespan=lifespan)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies_router, prefix="/movies", tags=["Movies"])
# TV Series will be implemented later
# app.include_router(tv_shows_router, prefix="/tv_shows", tags=["TVShows"])
app.include_router(ask_ai, prefix="/ask_ai", tags=["AI"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    logger.info("Starting backend server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
