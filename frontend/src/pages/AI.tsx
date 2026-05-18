import type { Media } from '../services/types';
import MovieCard from '../components/MovieCard';
import { useEffect, useState } from 'react';
import '../css/AI.css';
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
            <div>
                { answerAI.length > 0 ? answerAI : ''}
            </div>
            <div className='movies-grid'>
                {movies.map((movie) => getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;