# Play Assist

An AI-powered movie discovery app: browse and search movies sourced from
[TMDB](https://www.themoviedb.org/), and ask a Retrieval-Augmented Generation
(RAG) agent for personalized recommendations backed by vector similarity
search over movie embeddings.

- **Frontend** — React 19 + TypeScript + Vite ([details](frontend/README.md))
- **Backend** — Python FastAPI + PostgreSQL/pgvector + LangChain ([details](backend/README.md))

## Features

- Browse popular movies and search by title (TMDB-backed)
- JWT-based signup/login with access + refresh tokens
- "Ask AI" chat that recommends movies from a free-text query, using an LLM
  tool-calling agent + vector similarity search
- Admin-only settings page to bulk-import the latest popular movies

## Architecture

```mermaid
flowchart LR
    subgraph Client["Browser"]
        FE["React Frontend (Vite, :5173)"]
    end

    subgraph Server["Backend — FastAPI (:8000)"]
        Routes["routes/"] --> Services["services/"]
        Services --> Repos["db/respository/"]
        Services --> Agent["ai/movie_rag_agent.py"]
    end

    PG[("PostgreSQL + pgvector\n:5432")]
    Ollama[("Ollama\nnomic-embed-text\n:11434")]
    Anthropic[("Anthropic Claude API")]
    TMDB[("TMDB API")]

    FE -- "REST/JSON + JWT bearer token" --> Routes
    Repos --> PG
    Agent --> Ollama
    Agent --> Anthropic
    Services -- "fetch movie metadata" --> TMDB
```

See [backend/README.md](backend/README.md) for the layered backend
architecture, the auth sequence diagram, and the RAG recommendation flow in
detail.

## Prerequisites

**Option A — Docker (recommended):** Docker + Docker Compose. Nothing else
needs to be installed locally.

**Option B — manual/local setup:** Python 3.11+, Node.js 20+ with
[pnpm](https://pnpm.io/), a local PostgreSQL with the
[pgvector](https://github.com/pgvector/pgvector) extension, and
[Ollama](https://ollama.com/).

**Either way, you'll need:**
- A [TMDB API key](https://www.themoviedb.org/settings/api)
- An [Anthropic API key](https://console.anthropic.com/)

## Quick start (Docker Compose)

1. Copy the example env file and fill in your keys:

   ```bash
   cp .env.example .env
   ```

   At minimum set `TMDB_API_KEY`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`
   (e.g. `claude-sonnet-4-5`), and a random `JWT_SECRET`. See
   [Environment variables](#environment-variables) below for the full list.

2. Start everything:

   ```bash
   docker compose up --build
   ```

   This brings up, in order: Ollama (and pulls the `nomic-embed-text`
   embedding model automatically via the `ollama-init` container),
   PostgreSQL with pgvector, the FastAPI backend, and the Vite frontend.

3. Open the app:

   - Frontend: <http://localhost:5173>
   - Backend API docs: <http://localhost:8000/docs>

4. Log in with the seeded default admin account (created automatically on
   first backend startup):

   - Email: value of `ADMIN_EMAIL` (default `admin@playassist.com`)
   - Password: value of `ADMIN_PASSWORD` (default `password`)

   Or sign up a new account via the app's Sign Up form.

5. From **Settings** (visible to admins only), click **Load latest movies**
   to import popular movies from TMDB — otherwise the movie list/search/AI
   recommendations will be empty until you do.

To stop everything: `docker compose down` (add `-v` to also drop the
Postgres/Ollama volumes).

## Run without Docker (manual setup)

1. **PostgreSQL + pgvector** — run a Postgres instance with the `vector`
   extension available (the app runs `CREATE EXTENSION IF NOT EXISTS vector`
   itself on startup, so you don't need to create it manually — the extension
   just needs to be installed on the server, e.g. via the
   `pgvector/pgvector` Docker image, or `docker compose up db`).

2. **Ollama** — install and run Ollama locally, then pull the embedding
   model:

   ```bash
   ollama pull nomic-embed-text
   ```

3. **Environment variables** — copy `.env.example` to `.env` and fill in
   your keys. For a non-Docker run, point `DATABASE_URL` and `OLLAMA_BASE_URL`
   at `localhost` instead of the Docker service names `db`/`ollama`, e.g.:

   ```
   DATABASE_URL="postgresql://admin:password@localhost:5432/play_assist_db"
   OLLAMA_BASE_URL="http://localhost:11434"
   ```

4. **Backend** — see [backend/README.md](backend/README.md#running-locally-without-docker)
   for full steps:

   ```bash
   cd backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   set -a && source ../.env && set +a   # backend reads env vars directly, no .env auto-loading
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Frontend** — see [frontend/README.md](frontend/README.md#running-locally-without-docker):

   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```

   The frontend expects the backend at `http://127.0.0.1:8000` (hardcoded in
   `frontend/src/services/api.ts`).

## Environment variables

Defined in `.env` (see `.env.example` for a template). Consumed by the
backend via `utility/utils.get_env_key()`, and by `docker-compose.yaml` for
service configuration.

| Variable | Used by | Description |
|---|---|---|
| `TMDB_API_KEY` | backend | API key for TMDB movie/TV metadata |
| `ANTHROPIC_API_KEY` | backend | API key for the Claude chat model |
| `ANTHROPIC_MODEL` | backend | Claude model id (e.g. `claude-sonnet-4-5`) |
| `OLLAMA_BASE_URL` | backend | Base URL of the Ollama server |
| `EMBED_MODEL` | backend | Ollama embedding model name (default `nomic-embed-text`) |
| `VECTOR_SIZE` | backend | Embedding dimensionality (`768` for `nomic-embed-text`) — must match the embedding model |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | db container | Postgres credentials/database name |
| `DATABASE_URL` | backend | SQLAlchemy connection string to Postgres |
| `JWT_SECRET` | backend | Secret used to sign/verify JWTs — set to a random value |
| `JWT_ALGORITHM` | backend | JWT signing algorithm (`HS256`) |
| `ADMIN_FIRST_NAME` / `ADMIN_LAST_NAME` / `ADMIN_EMAIL` / `ADMIN_PASSWORD` | backend | Default admin user seeded on first startup |

## Project structure

```
play_assist/
├── backend/          # FastAPI app — see backend/README.md
├── frontend/         # React app — see frontend/README.md
├── docker-compose.yaml
├── .env.example
└── README.md         # you are here
```

## Further reading

- [backend/README.md](backend/README.md) — layered architecture, auth
  sequence diagram, RAG recommendation flow, API endpoint reference
- [frontend/README.md](frontend/README.md) — routing, state management, API
  integration details
