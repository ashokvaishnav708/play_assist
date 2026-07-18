/**
 * Thin fetch wrapper for the backend API: token storage, an authenticated
 * fetch with automatic silent refresh-on-401, and one function per endpoint.
 */
import type { Media, AIQueryResponse, User, TokenPair, AuthResponse } from "./types";

const API_BASE_URL = "http://127.0.0.1:8000";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

// Dispatched whenever a session can no longer be refreshed, so AuthContext
// can drop back to a logged-out state regardless of which call noticed it.
export const AUTH_LOGOUT_EVENT = "auth:logout";

/** Read the stored access token, or null if the user isn't logged in. */
export function getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}

/** Read the stored refresh token, or null if none is stored. */
function getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
}

/** Persist a freshly issued access/refresh token pair to localStorage. */
function setTokens(tokens: TokenPair) {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

/** Remove any stored tokens (used on logout or when refresh fails). */
function clearTokens() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
}

/** Extract a human-readable error message from a failed response, or fall back. */
async function parseErrorDetail(response: Response, fallback: string): Promise<string> {
    try {
        const error = await response.json();
        return error.detail || fallback;
    } catch {
        return fallback;
    }
}

/** Exchange the stored refresh token for a new token pair, storing the result. */
async function refreshAccessToken(): Promise<string> {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        throw new Error("No refresh token available");
    }

    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
        throw new Error("Refresh failed");
    }

    const tokens: TokenPair = await response.json();
    setTokens(tokens);
    return tokens.access_token;
}

// Attaches the access token, and on a 401 tries exactly one silent refresh
// before giving up and forcing the app back to a logged-out state.
async function authFetch(path: string, init: RequestInit = {}, isRetry = false): Promise<Response> {
    const accessToken = getAccessToken();
    const headers = new Headers(init.headers);
    if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`);
    }

    const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });

    if (response.status === 401 && !isRetry && getRefreshToken()) {
        try {
            await refreshAccessToken();
        } catch {
            clearTokens();
            window.dispatchEvent(new CustomEvent(AUTH_LOGOUT_EVENT));
            return response;
        }
        return authFetch(path, init, true);
    }

    return response;
}

/** Log in with email/password, storing the returned tokens on success. */
export async function loginUser(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
        throw new Error(await parseErrorDetail(response, "Login failed"));
    }

    const data: AuthResponse = await response.json();
    setTokens(data);
    return data;
}

/** Create a new user account. Does not log the user in. */
export async function signupUser(email: string, password: string, firstName: string, lastName: string): Promise<User> {
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
        throw new Error(await parseErrorDetail(response, "Sign up failed"));
    }

    return await response.json();
}

/** Log out on the backend (invalidating tokens) and always clear local tokens. */
export async function logoutUser(): Promise<void> {
    try {
        if (getAccessToken()) {
            await authFetch("/auth/logout", { method: "POST" });
        }
    } finally {
        // Always drop local tokens, even if the network call failed - the
        // user's intent to log out of this browser should never get stuck.
        clearTokens();
    }
}

/** Fetch the currently authenticated user's profile. */
export async function getMe(): Promise<User> {
    const response = await authFetch("/auth/me");

    if (!response.ok) {
        throw new Error(await parseErrorDetail(response, "Not authenticated"));
    }

    return await response.json();
}

/** Fetch the first page of currently popular movies. */
export async function getPopularMovies(): Promise<Media[]> {
    const response = await authFetch("/movies/movies");
    const data = await response.json();
    return data.movies;
}

/** Search movies by free-text query. */
export async function searchMovies(query: string): Promise<Media[]> {
    const response = await authFetch(`/movies/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.movies;
}

/** Ask the AI recommendation agent a free-text movie question. */
export async function askAI(question: string): Promise<AIQueryResponse> {
    const response = await authFetch("/ask_ai/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question })
    });
    const data = await response.json();
    return data;
}

/** Trigger the backend to import the latest popular movies from TMDB (admin action). */
export async function fetchLatestMovies() {
    const response = await authFetch("/movies/load_movies");
    if (!response.ok) {
        throw Error("Failed to load movies.");
    }

    const data = await response.json();
    return data.movies;
}
