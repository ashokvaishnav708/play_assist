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