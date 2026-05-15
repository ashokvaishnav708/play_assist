import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import type { Media } from "../services/types";

type MovieContextType = {
    favorites: Media[];
    addFavorite: (movie: Media) => void;
    removeFavorite: (movieId: number) => void;
    isFavorite: (movieId: number) => boolean;
}

const MovieContext = createContext<MovieContextType>(null as unknown as MovieContextType);

export function useMovieContext() {
    return useContext(MovieContext);
}

export function MovieProvider({ children }: { children: ReactNode }) {
    const [favorites, setFavorites] = useState<Media[]>([]);

    useEffect(() => {
        const storedFavs = localStorage.getItem('favorites');

        if (storedFavs) {
            setFavorites(JSON.parse(storedFavs));
        }
    }, []);

    useEffect(() => {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    }, [favorites]);

    function addFavorite(movie: Media) {
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