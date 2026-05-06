import type { Movie } from "./types";
import '../css/MovieCard.css';
import { useMovieContext } from "../contexts/MovieContext";

function MovieCard(movie: Movie) {
    const { isFavorite, addFavorite, removeFavorite } = useMovieContext();
    function onFavoriteClick() {
        alert('Favorite clicked!!');
    }

    return (
        <div className="movie-card">
            <div className="movie-poster">
                <img src={ movie.url } alt={ movie.title } />
                <div>
                    <button className="favorite-btn" onClick={onFavoriteClick} >
                        🤍
                        {/* ❤️ */}
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