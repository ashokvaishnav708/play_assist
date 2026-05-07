import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from movies import router as movies_router
from tv_shows import router as tv_shows_router

DEBUG = True

app = FastAPI(debug=DEBUG)

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(movies_router, prefix="/movies", tags=["Movies"])
app.include_router(tv_shows_router, prefix="/tv_shows", tags=["TVShows"])
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
