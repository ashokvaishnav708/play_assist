import type { Media } from '../services/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
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
        <div className='p-8 w-full'>
            <form onSubmit={ handleSearch } className='max-w-2xl mx-auto mb-8 flex gap-4 px-4'>
                <input 
                    type='text' 
                    className='flex-1 px-4 py-3 border-none rounded bg-gray-700 text-white text-base focus:outline-none focus:ring-2 focus:ring-gray-600' 
                    placeholder='Search for movies...'
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type='submit' className='px-6 py-3 bg-red-600 text-white rounded font-medium transition-colors duration-200 hover:bg-red-700 whitespace-nowrap' >Search</button>
            </form>
            <div className='grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6 p-4 w-full'>
                {movies.map((movie) => getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;