export type Media = {
    id: number;
    title: string
    release_date: string
    poster_path?: string
    original_language: string
    overview: string
};

export type AIQueryResponse = {
    answer: string;
    movies: Media[];
}

export type User = {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    created_at: string;
};

export type TokenPair = {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
};

export type AuthResponse = TokenPair & {
    user: User;
};