import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from movies import router as movies_router
from tv_shows import router as tv_shows_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DEBUG = True

app = FastAPI(debug=DEBUG)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
    ]

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(movies_router, prefix="/movies", tags=["Movies"])
app.include_router(tv_shows_router, prefix="/tv_shows", tags=["TVShows"])

if __name__ == "__main__":
    logger.info("Starting backend server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
