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
        <div className='w-full min-h-[calc(100vh-80px)] bg-linear-to-b from-gray-900 via-gray-800 to-black'>
            <div className='max-w-7xl mx-auto px-4 py-8'>
                {/* Hero Section */}
                <div className='mb-12'>
                    <h1 className='text-5xl md:text-6xl font-bold text-white mb-4'>
                        Discover Movies
                    </h1>
                    <p className='text-gray-400 text-lg mb-8'>Search through thousands of movies and find your next favorite</p>
                    
                    <form onSubmit={ handleSearch } className='flex gap-3 max-w-xl'>
                        <input 
                            type='text' 
                            className='flex-1 px-6 py-4 border-none rounded-lg bg-gray-800 text-white text-base placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all' 
                            placeholder='Search for movies...'
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                        <button type='submit' className='px-8 py-4 bg-linear-to-r from-red-600 to-red-500 text-white rounded-lg font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-red-500/50 whitespace-nowrap' >
                            {loading ? 'Searching...' : 'Search'}
                        </button>
                    </form>
                </div>

                {/* Results Section */}
                {error && (
                    <div className='bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-8 text-red-300'>
                        {error}
                    </div>
                )}

                <div className='mb-6'>
                    <h2 className='text-2xl font-bold text-white mb-6'>
                        {searchQuery ? `Results for "${searchQuery}"` : 'Popular Movies'}
                    </h2>
                    <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
                        {loading && !movies.length ? (
                            <div className='col-span-full text-center text-gray-400 py-12'>
                                <p className='text-xl'>Loading movies...</p>
                            </div>
                        ) : movies.length > 0 ? (
                            movies.map((movie) => getMovieCard(movie))
                        ) : (
                            <div className='col-span-full text-center text-gray-400 py-12'>
                                <p className='text-xl'>No movies found</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;