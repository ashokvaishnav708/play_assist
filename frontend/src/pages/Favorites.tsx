import '../css/Favorites.css';
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
            <div className='movies-grid'>
                {
                    favorites.map((movie) => getMovieCard(movie))
                }
            </div>
        );
    }


    return (
        <div className='favorites-empty'>
            <h2> No Favorite movies yet.</h2>
            <p>Start adding movies to your favorites and they will appear here!</p>
        </div>
    );
}

export default Favorites;