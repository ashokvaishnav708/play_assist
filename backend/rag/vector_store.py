from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from typing import List
from logging import getLogger

logger = getLogger(__name__)

class MovieVectorStore:
    def __init__(self, google_api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", google_api_key=google_api_key)
        self.vector_store: InMemoryVectorStore = None

    def build(self, documents: List[Document]):
        try:
            self.vector_store = InMemoryVectorStore.from_documents(documents=documents, embedding=self.embeddings)
            logger.info(f"Vector store build with {len(documents)} movies.")
        except Exception as e:
            logger.error(f"Error while building vector store due to {e}.")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Cannot perform search.")
        return self.vector_store.similarity_search(query, k=k)
    
    def get_reteiver(self, k: int = 4) -> VectorStoreRetriever:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Cannot get retreiver.")
        return self.vector_store.as_retriever(kwargs={"k": k})