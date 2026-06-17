import { useMovieContext } from '../contexts/MovieContext';
import MovieCard from '../components/MovieCard';
import type { Media } from '../services/types';

function Favorites()  {

    const { favorites } = useMovieContext();

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
            <div className='grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6 p-4 w-full'>
                {
                    favorites.map((movie) => getMovieCard(movie))
                }
            </div>
        );
    }


    return (
        <div className='text-center p-8 bg-white/5 rounded-xl mx-auto my-8 max-w-2xl'>
            <h2 className='mb-4 text-3xl text-red-600'> No Favorite movies yet.</h2>
            <p className='text-gray-400 text-xl leading-relaxed'>Start adding movies to your favorites and they will appear here!</p>
        </div>
    );
}

export default Favorites;