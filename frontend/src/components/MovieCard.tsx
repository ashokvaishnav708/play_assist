import type { Movie } from "./types";
import '../css/MovieCard.css';
import { useMovieContext } from "../contexts/MovieContext";

function MovieCard(movie: Movie) {
    const { isFavorite, addFavorite, removeFavorite } = useMovieContext();

    const favorite = isFavorite(movie.id);

    function onFavoriteClick(e: Event) {
        e.preventDefault();
        if (favorite) removeFavorite(movie.id);
        else addFavorite(movie);
    }

    return (
        <div className="movie-card">
            <div className="movie-poster">
                <img src={ movie.url } alt={ movie.title } />
                <div>
                    <button className={`favorite-btn ${favorite ? "active": ""}`} onClick={ onFavoriteClick } >
                        🤍
                    </button>
                </div>
            </div>
            <div className="movie-info">
                <h3>{movie.title}</h3>
                <p>{movie.releaseDate}</p>
            </div>
        </div>
    );
}

export default MovieCard;