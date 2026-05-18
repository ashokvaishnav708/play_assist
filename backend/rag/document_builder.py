from langchain_core.documents import Document
from models.movies import Movie
from typing import List

def movie_to_document(movie: Movie) -> Document:
    content = f"""
    Title: {movie.title}
    Poster: {movie.poster_path}
    Overview: {movie.overview}
    Release Date: {movie.release_date}
    Original Language: {movie.original_language}
    """.strip()

    metadata = {
        "id": movie.id,
        "title": movie.title,
        "poster_path": movie.poster_path,
        "overview": movie.overview,
        "release_date": movie.release_date,
        "original_language": movie.original_language
    }

    return Document(page_content=content, metadata=metadata)

def movies_to_documents(movies: List[Movie]) -> List[Document]:
    return [movie_to_document(movie) for movie in movies]
