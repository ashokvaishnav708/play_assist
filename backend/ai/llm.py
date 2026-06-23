from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from utility.utils import get_env_key

GOOGLE_API_KEY = get_env_key("GEMINI_API_KEY")

def get_llm_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=GOOGLE_API_KEY, temperature=0.1)

def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", google_api_key=GOOGLE_API_KEY)