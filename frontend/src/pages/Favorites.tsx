import { useMovieContext } from '../contexts/MovieContext';
import MovieCard from '../components/MovieCard';
import type { Media } from '../services/types';

/**
 * Favorites page: lists the user's saved movies (from MovieContext /
 * localStorage), or an empty-state message when there are none.
 *
 * Note: not currently routed in App.tsx (route is commented out).
 */
function Favorites()  {

    const { favorites } = useMovieContext();

    /** Render a single favorite as a MovieCard. */
    function getMovieCard(movie: Media) {
        return <MovieCard 
                    id={movie.id} 
                    key={movie.id} 
                    title={movie.title} 
                    overview={movie.overview} 
                    release_date={movie.release_date} 
                    poster_path={movie.poster_path} 
                    original_language={movie.original_language}
                />;
    }

    if (favorites && favorites.length) {
        return (
            <div className='w-full min-h-[calc(100vh-80px)] bg-linear-to-b from-gray-900 via-gray-800 to-black'>
                <div className='max-w-7xl mx-auto px-4 py-8'>
                    <h1 className='text-5xl md:text-6xl font-bold text-white mb-2'>
                        ❤️ Your Favorites
                    </h1>
                    <p className='text-gray-400 text-lg mb-8'>
                        {favorites.length} movie{favorites.length !== 1 ? 's' : ''} added to your collection
                    </p>

                    <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
                        {
                            favorites.map((movie) => getMovieCard(movie))
                        }
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className='w-full min-h-[calc(100vh-80px)] bg-linear-to-b from-gray-900 via-gray-800 to-black flex items-center justify-center px-4'>
            <div className='text-center'>
                <div className='mb-6'>
                    <span className='text-7xl'>🎬</span>
                </div>
                <h2 className='mb-4 text-4xl font-bold text-white'>No Favorite Movies Yet</h2>
                <p className='text-gray-400 text-lg leading-relaxed max-w-md'>
                    Start exploring movies and TV shows, then add your favorites to build your personal collection!
                </p>
            </div>
        </div>
    );
}

export default Favorites;