from models.movie import MovieCreateRequest as Movie

from typing import List

class Movies:
    def __init__(self):
        self.__movies: List[Movie] = []

    def get_movies(self) -> List[Movie]:
        return self.__movies
    
    def add_movie(self, movie: Movie) -> None:
        self.__movies.append(movie)

    def add_movies(self, movies: list[Movie]) -> None:
        self.__movies = [*self.__movies, *movies]


movie_store = Movies()

