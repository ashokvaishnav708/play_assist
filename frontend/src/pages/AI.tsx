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
        <div className='p-8 w-full'>
            <form onSubmit={ handleSearch } className='max-w-2xl mx-auto mb-8 flex gap-4 px-4'>
                <input 
                    type='text' 
                    className='flex-1 px-4 py-3 border-none rounded bg-gray-700 text-white text-base focus:outline-none focus:ring-2 focus:ring-gray-600' 
                    placeholder='Ask me anything about movies or TV shows...'
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type='submit' className='px-6 py-3 bg-red-600 text-white rounded font-medium transition-colors duration-200 hover:bg-red-700 whitespace-nowrap' >Ask</button>
            </form>
            <div>
                { answerAI.length > 0 ? answerAI : ''}
            </div>
            <div className='grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6 p-4 w-full'>
                {movies.map((movie) => getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;