import type { Media } from '../services/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
import { askAI } from '../services/api';

function Home() {
    const [searchQuery, setSearchQuery] = useState("");

    const [movies, setMovies] = useState<Media[]>([]);
    const [answerAI, setAnswerAI] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

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
            const { answer, movies } = await askAI(searchQuery);
            setAnswerAI(answer);
            setMovies(movies);
            setError(null);
        }catch(err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    }
    
    return (
        <div className='w-full min-h-[calc(100vh-80px)] bg-gradient-to-b from-gray-900 via-gray-800 to-black'>
            <div className='max-w-7xl mx-auto px-4 py-8'>
                {/* Hero Section */}
                <div className='mb-12'>
                    <h1 className='text-5xl md:text-6xl font-bold text-white mb-4'>
                        🤖 Ask AI
                    </h1>
                    <p className='text-gray-400 text-lg mb-8'>Get personalized movie and TV show recommendations powered by AI</p>
                    
                    <form onSubmit={ handleSearch } className='flex gap-3 max-w-2xl'>
                        <input 
                            type='text' 
                            className='flex-1 px-6 py-4 border-none rounded-lg bg-gray-800 text-white text-base placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all' 
                            placeholder='Ask me anything about movies or TV shows...'
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                        <button type='submit' className='px-8 py-4 bg-gradient-to-r from-red-600 to-red-500 text-white rounded-lg font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-red-500/50 whitespace-nowrap' >
                            {loading ? 'Asking...' : 'Ask'}
                        </button>
                    </form>
                </div>

                {/* AI Response */}
                {answerAI.length > 0 && (
                    <div className='mb-12 bg-gradient-to-r from-red-900/20 to-purple-900/20 border border-red-500/30 rounded-lg p-8 backdrop-blur-sm'>
                        <h2 className='text-xl font-bold text-white mb-4'>AI Response</h2>
                        <p className='text-gray-200 leading-relaxed'>{answerAI}</p>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className='text-center py-12'>
                        <div className='inline-block'>
                            <div className='animate-spin rounded-full h-12 w-12 border-4 border-gray-600 border-t-red-600'></div>
                        </div>
                        <p className='text-gray-400 mt-4'>AI is thinking...</p>
                    </div>
                )}

                {/* Results Section */}
                {movies.length > 0 && (
                    <div className='mb-6'>
                        <h2 className='text-2xl font-bold text-white mb-6'>
                            Recommended Movies & Shows
                        </h2>
                        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
                            {movies.map((movie) => getMovieCard(movie))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Home;