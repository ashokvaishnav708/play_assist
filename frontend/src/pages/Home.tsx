import type { Movie } from '../components/types';
import MovieCard from '../components/MovieCard';
import { useState } from 'react';
import '../css/Home.css';

function Home() {
    const [searchQuery, setSearchQuery] = useState("");

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
        return <MovieCard id={movie.id} key={movie.id} title={movie.title} description={movie.description} releaseDate={movie.releaseDate} />;
    }

    function handleSearch(e: Event) {
        e.preventDefault();
        alert(searchQuery);
    }
    
    return (
        <div className='home'>
            <form onSubmit={handleSearch} className='search-form'>
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
                {movies.map((movie) => movie.title.toLowerCase().startsWith(searchQuery.toLowerCase()) && getMovieCard(movie))}
            </div>
        </div>
    );
}

export default Home;