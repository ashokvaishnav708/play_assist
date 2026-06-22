import type { Media, AIQueryResponse } from "./types";

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

export async function askAI(question: string): Promise<AIQueryResponse> {
    const response = await fetch(`${API_BASE_URL}/ask_ai/query_agent`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question })
    });
    const data = await response.json();
    return data;
}

export async function loginUser(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
    }
    
    return await response.json();
}

export async function signupUser(email: string, password: string, firstName: string, lastName: string) {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,
            password,
            first_name: firstName,
            last_name: lastName
        })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Sign up failed");
    }
    
    return await response.json();
}
