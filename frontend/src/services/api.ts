import type { Media } from "./types";

const API_BASE_URL = "http://127.0.0.1:8000";


export async function getPopularMovies(): Promise<Media[]> {
    const response = await fetch(`${API_BASE_URL}/movies/popular`);
    const data = await response.json();
    return data.movies;
}

export async function searchMovies(query: string): Promise<Media[]> {
    const response = await fetch(`${API_BASE_URL}/movies/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.movies;
}
