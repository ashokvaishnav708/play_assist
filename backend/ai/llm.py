from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from utility.utils import get_env_key

GOOGLE_API_KEY = get_env_key("GEMINI_API_KEY")

def get_llm_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=GOOGLE_API_KEY, temperature=0.1)

def get_embedding_model(is_query: bool = False) -> GoogleGenerativeAIEmbeddings:
    task_type = "retrieval_query" if is_query else "retrieval_document"
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", google_api_key=GOOGLE_API_KEY, task_type=task_type)