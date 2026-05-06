import { createContext, useContext, useEffect, useState, Provider } from "react"
import type { Movie } from "../components/types";

const MovieContext = createContext({});

export function useMovieContext() {
    return useContext(MovieContext);
}

export function MovieProvider(children) {
    const [favorites, setFavorites] = useState<Movie[]>([]);

    useEffect(() => {
        const storedFavs = localStorage.getItem('favorites');

        if (storedFavs) {
            setFavorites(JSON.parse(storedFavs));
        }
    }, []);

    useEffect(() => {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }, [favorites]);

    function addFavorite(movie: Movie) {
        setFavorites(prev => [...prev, movie]);
    }

    function removeFavorite(movieId: number) {
        setFavorites(prev => prev.filter(movie => movie.id !== movieId));
    }

    function isFavorite(movieId: number) {
        return favorites.some(movie => movie.id === movieId);
    }

    const value = {
        favorites,
        addFavorite,
        removeFavorite,
        isFavorite,
    };

    return (
        <MovieContext.Provider value={value}>
            {children}
        </MovieContext.Provider>
    );
}