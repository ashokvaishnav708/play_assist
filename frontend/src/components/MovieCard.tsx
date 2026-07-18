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
        <div className="group relative rounded-xl overflow-hidden bg-gray-900/50 backdrop-blur-sm border border-gray-800 transition-all duration-300 hover:border-red-500/50 hover:shadow-xl hover:shadow-red-500/20 h-[542px] flex flex-col hover:-translate-y-2">
            <div className="relative w-full flex-1 overflow-hidden bg-gray-800">
                <img src={ movie.poster_path } alt={ movie.title } className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" />
                

                <div className="absolute inset-0 bg-linear-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                {/* Favorite Button */}
                {/* <button 
                    className={`absolute top-4 right-4 text-2xl p-2 bg-black/60 rounded-full w-12 h-12 flex items-center justify-center transition-all duration-200 hover:bg-black/90 backdrop-blur-sm border border-gray-700/50 ${favorite ? 'text-red-500 bg-red-500/20 border-red-500/50' : 'text-white hover:text-red-500'}`} 
                    onClick={ onFavoriteClick }
                >
                    { favorite ? "❤️" : "🤍" }
                </button> */}
            </div>

            {/* Content Section */}
            <div className="p-4 flex flex-col gap-2 bg-linear-to-t from-gray-900 to-gray-900/50 border-t border-gray-800">
                <h3 className="text-base font-semibold text-white m-0 line-clamp-2 group-hover:text-red-400 transition-colors">
                    {movie.title}
                </h3>
                <p className="text-gray-500 text-sm">
                    {movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}
                </p>
                {movie.original_language && (
                    <p className="text-xs text-gray-600 uppercase tracking-wide">
                        🌐 {movie.original_language}
                    </p>
                )}
            </div>
        </div>
    );
}

export default MovieCard;