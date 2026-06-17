import type { Media } from '../services/types';
import { useMovieContext } from "../contexts/MovieContext";

function MovieCard(movie: Media) {
    const { isFavorite, addFavorite, removeFavorite } = useMovieContext();

    const favorite = isFavorite(movie.id);

    function onFavoriteClick(e: Event) {
        e.preventDefault();
        if (favorite) removeFavorite(movie.id);
        else addFavorite(movie);
    }

    return (
        <div className="relative rounded-lg overflow-hidden bg-gray-900 transition-transform duration-200 h-[542px] w-[300px] hover:-translate-y-1 flex flex-col">
            <div className="relative w-full aspect-video">
                <img src={ movie.poster_path } alt={ movie.title } className="w-full h-full object-cover" />
                <div>
                    <button className={`absolute top-4 right-4 text-white text-xl p-2 bg-black/50 rounded-full w-10 h-10 flex items-center justify-center transition-colors duration-200 hover:bg-black/80 ${favorite ? 'text-red-600' : ''}`} onClick={ onFavoriteClick } >
                        { favorite ? "❤️" : "🤍" }
                    </button>
                </div>
            </div>
            <div className="p-4 flex-1 flex flex-col gap-2">
                <h3 className="text-base m-0">{movie.title}</h3>
                <p className="text-gray-400 text-sm">{movie.release_date}</p>
            </div>
        </div>
    );
}

export default MovieCard;