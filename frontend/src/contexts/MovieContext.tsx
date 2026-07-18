/**
 * Global favorites state, persisted to localStorage. Wrap the app in
 * <MovieProvider> and read/mutate favorites via `useMovieContext()`.
 */
import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import type { Media } from "../services/types";

/** Shape of the value exposed by MovieContext / useMovieContext(). */
type MovieContextType = {
    favorites: Media[];
    addFavorite: (movie: Media) => void;
    removeFavorite: (movieId: number) => void;
    isFavorite: (movieId: number) => boolean;
}

const MovieContext = createContext<MovieContextType>(null as unknown as MovieContextType);

/** Hook for consuming favorites state/actions anywhere under <MovieProvider>. */
export function useMovieContext() {
    return useContext(MovieContext);
}

/** Provides favorites state to the app, backed by localStorage. */
export function MovieProvider({ children }: { children: ReactNode }) {
    const [favorites, setFavorites] = useState<Media[]>([]);

    // Load any previously saved favorites once, on mount.
    useEffect(() => {
        const storedFavs = localStorage.getItem('favorites');

        if (storedFavs) {
            setFavorites(JSON.parse(storedFavs));
        }
    }, []);

    // Persist favorites to localStorage whenever they change.
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