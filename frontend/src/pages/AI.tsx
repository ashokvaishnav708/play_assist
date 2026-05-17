import type { Media } from '../services/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
import '../css/AI.css';
import { searchMovies, loadMovieSeeds } from '../services/api';

function Home() {
    const [searchQuery, setSearchQuery] = useState("");

    const [movies, setMovies] = useState<Media[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    function getMovieCard(movie: Media) {
        return <MovieCard 
            id={movie.id} 
            key={movie.id} 
            title={movie.title} 
            overview={movie.overview} 
            release_date={movie.release_date} 
            original_language={movie.original_language}
            poster_path={movie.poster_path}
        />;
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

    async function handleSeedsLoading(e: Event) {
        e.preventDefault();
        const isSeedLoaded = await loadMovieSeeds();
        console.log(isSeedLoaded);
    }
    
    return (
        <div className='home'>
            <button onClick={ handleSeedsLoading }>Load seeds</button>
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