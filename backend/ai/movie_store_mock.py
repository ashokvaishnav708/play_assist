"""In-memory movie store used for local testing/mocking without a database."""

from models.movie import MovieCreateRequest as Movie

from typing import List


class MovieStoreMock:
    """Keeps a plain in-memory list of movies as a stand-in for the real repository."""

    def __init__(self):
        self.__movies: List[Movie] = []

    def get_movies(self) -> List[Movie]:
        """Return all movies currently held in memory."""
        return self.__movies

    def add_movie(self, movie: Movie) -> None:
        """Append a single movie to the in-memory store."""
        self.__movies.append(movie)

    def add_movies(self, movies: list[Movie]) -> None:
        """Append multiple movies to the in-memory store."""
        self.__movies = [*self.__movies, *movies]


# Module-level singleton instance for callers that want a shared mock store.
movie_store = MovieStoreMock()

