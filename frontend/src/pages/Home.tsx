import type { Media } from '../services/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
import '../css/Home.css';
import { searchMovies, getPopularMovies } from '../services/api';

function Home() {
    const [searchQuery, setSearchQuery] = useState("");

    const [movies, setMovies] = useState<Media[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadPopularMovies() {
            try {
                const popularMovies = await getPopularMovies();
                setMovies(popularMovies);
                setError(null);
            } catch (error) {
                console.log(error);
                setError("Failed to load movies...")
            } finally {
                setLoading(false);
            }
        }
        loadPopularMovies();
    }, []);

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
            <form onSubmit={ handleSearch } className='search-form'>
                <input 
                    type='text' 
                    className='search-input' 
                    placeholder='Search for movies...'
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type='submit' className='search-button' >Search</button>
            </form>
            <div className='movies-grid'>
                {movies.map((movie) => getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;