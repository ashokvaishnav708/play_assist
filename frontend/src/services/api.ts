const API_URL = "localhost:8000";

export async function getPopularMovies() {
    const response = await fetch(`${API_URL}/movie/popular`);
    const data = await response.json();
    return data.results;
}

export async function searchMovies(query: string) {
    const response = await fetch(`${API_URL}/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.result;
}