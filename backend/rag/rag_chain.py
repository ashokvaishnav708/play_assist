from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from utility.utils import get_env_key

from rag.document_builder import movies_to_documents
from models.movie import MovieCreateRequest as Movie

from typing import List, Tuple


from logging import getLogger
logger = getLogger(__name__)

MOVIE_RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert movie advisor. Use the following movie information 
retrieved from the database to answer the user's question accurately.

Context:
{context}

Question: {question}

Answer based only on the provided context. If the answer is not in the context, 
say "I don't know about such media content."
"""
)

class RAGChain:
    def __init__(self, gemini_api_key: str):
        self.__embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview", google_api_key=gemini_api_key)
        self.__llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=gemini_api_key, temperature=0.3)
        self.__vector_store: InMemoryVectorStore  | None = None
        self.__chain: RetrievalQA | None = None
    
    def __build_vector_store(self, movies: List[Movie]):
        try:
            documents = movies_to_documents(movies)
            self.__vector_store = InMemoryVectorStore.from_documents(documents=documents, embedding=self.__embeddings)
            logger.debug(f"Vector store build with {len(documents)} movies.")
        except Exception as e:
            logger.error(f"Error while building vector store due to {e}.")

    def __similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self.__vector_store:
            raise ValueError("Vector store not initialized. Cannot perform search.")
        return self.__vector_store.similarity_search(query, k=k)
    
    def __get_retiever(self, k: int = 4) -> VectorStoreRetriever:
        if not self.__vector_store:
            raise ValueError("Vector store not initialized. Cannot get retreiver.")
        return self.__vector_store.as_retriever(kwargs={"k": k})
    
    def build_rag_chain(self, movies: List[Movie]):
        logger.info("Building RAG chain...")
        self.__build_vector_store(movies)
        retriever = self.__get_retiever()
        self.__chain = RetrievalQA.from_chain_type(
            llm=self.__llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": MOVIE_RAG_PROMPT},
            return_source_documents=True   
        )
        logger.info("RAG chain built successfully.")

    def query(self, query: str) -> Tuple[str, List[Movie]]:
        if not self.__chain:
            raise ValueError("RAG chain not initialized/built.")
        result = self.__chain.invoke({ "query": query })
        answer = result.get("result", 'No answer provided by AI.')
        source_documents: List[Document] = result.get("source_documents", [])
        movies = [Movie(**document.metadata) for document in source_documents]
        return (answer, movies)


GOOGLE_API_KEY = get_env_key("GEMINI_API_KEY")

rag_chain = RAGChain(gemini_api_key=GOOGLE_API_KEY)

