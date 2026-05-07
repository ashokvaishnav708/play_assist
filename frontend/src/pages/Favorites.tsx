import '../css/Favorites.css';
import { useMovieContext } from '../contexts/MovieContext';
import MovieCard from '../components/MovieCard';

function Favorites()  {

    const { favorites } = useMovieContext();

    if (favorites) {
        return (
            <div className='movies-grid'>
                {
                    // TODO: Add movie card component properly
                    favorites.map((movie) => <MovieCard />)
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