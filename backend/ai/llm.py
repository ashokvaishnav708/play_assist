"""Factory helpers for the LLM chat model and embedding model, cached as
process-wide singletons so the SDK clients are constructed only once."""

from langchain_anthropic import ChatAnthropic
from langchain_ollama import OllamaEmbeddings
from utility.utils import get_env_key

from logging import getLogger

logger = getLogger(__name__)

ANTHROPIC_API_KEY = get_env_key("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = get_env_key("ANTHROPIC_MODEL")

OLLAMA_BASE_URL = get_env_key("OLLAMA_BASE_URL")
EMBED_MODEL = get_env_key("EMBED_MODEL")

# Lazily-initialized module-level singletons, shared across all requests.
_LLM: ChatAnthropic | None = None
_EMBEDDINGS: OllamaEmbeddings | None = None


def get_llm_model() -> ChatAnthropic:
    """Return the shared Anthropic chat model, creating it on first call."""
    global _LLM

    if _LLM is None:
        logger.info(
            f"Initializing LLM model with model={ANTHROPIC_MODEL} from Anthropic."
        )
        _LLM = ChatAnthropic(
            model=ANTHROPIC_MODEL,
            api_key=ANTHROPIC_API_KEY,
            thinking={"type": "adaptive"},
        )

    return _LLM


def get_embedding_model() -> OllamaEmbeddings:
    """Return the shared Ollama embedding model, creating it on first call."""
    global _EMBEDDINGS

    if _EMBEDDINGS is None:
        logger.info(
            f"Initializing OllamaEmbeddings with model={EMBED_MODEL} at {OLLAMA_BASE_URL}"
        )
        _EMBEDDINGS = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    return _EMBEDDINGS
