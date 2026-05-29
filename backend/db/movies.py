from db.models import Movie as DBMovie
from db.database import get_db

from models.movies import Movie

from typing import List

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
