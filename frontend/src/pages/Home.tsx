import type { Movie } from '../components/types';
import MovieCard from '../components/MovieCard';

function Home() {
    const movies: Movie[] = [
        {
            id: 1, 
            title: "John Wick", 
            releaseDate: "2020", 
            description: "John Wick description"
        },
        {
            id: 2, 
            title: "Terminator", 
            releaseDate: "1999", 
            description: "Terminator description"
        },
        {
            id: 3, 
            title: "The Matrix", 
            releaseDate: "1998", 
            description: "The MAtrix description"
        }
    ];

    function getMovieCard(movie: Movie) {
        return <MovieCard id={movie.id} key={movie.id} title={movie.title} description={movie.description} releaseDate={movie.releaseDate} />
    }
    
    return (
        <div className='home'>
            <div className='movies-grid'>
                {movies.map((movie) => getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;