/** Shared types mirroring the backend's Pydantic response models. */

/** A movie/show as returned by the movies and AI endpoints. */
export type Media = {
    id: number;
    title: string
    release_date: string
    poster_path?: string
    original_language: string
    overview: string
};

/** Response from POST /ask_ai/query. */
export type AIQueryResponse = {
    answer: string;
    movies: Media[];
}

/** The authenticated user, as returned by /auth/me, /auth/login, /auth/signup. */
export type User = {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    created_at: string;
    is_admin: boolean;
};

/** Access/refresh token pair returned by login and token refresh. */
export type TokenPair = {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
};

/** Login response: a token pair plus the authenticated user. */
export type AuthResponse = TokenPair & {
    user: User;
};