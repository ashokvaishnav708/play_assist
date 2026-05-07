import type { Movie } from '../components/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
import '../css/AI.css';
import { searchMovies, getPopularMovies } from '../services/api';

function Home() {
    const [searchQuery, setSearchQuery] = useState("");

    const [movies, setMovies] = useState<Movie[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    function getMovieCard(movie: Movie) {
        return <MovieCard id={movie.id} key={movie.id} title={movie.title} description={movie.description} releaseDate={movie.releaseDate} />;
    }

    async function handleSearch(e: Event) {
        e.preventDefault();
        if (!searchQuery.trim()) return;
        if (loading) return;
        setLoading(true);

        try {
            const searchResults = await searchMovies(searchQuery);
            setMovies(searchResults);
            setError(null);
        }catch(err) {
            console.log(err);


        } finally {
            setLoading(false);
        }
    }
    
    return (
        <div className='home'>
            <form onSubmit={ handleSearch } className='ai-form'>
                <input 
                    type='text' 
                    className='ai-input' 
                    placeholder='Ask me anything about movies or TV shows...'
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type='submit' className='query-button' >Ask</button>
            </form>
            <div className='movies-grid'>
                {movies.map((movie) => movie.title.toLowerCase().startsWith(searchQuery.toLowerCase()) && getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;