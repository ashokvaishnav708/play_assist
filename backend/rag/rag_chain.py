from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores.base import VectorStoreRetriever


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

def build_rag_chain(retriever: VectorStoreRetriever, google_api_key: str) -> RetrievalQA:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=google_api_key,
        temperature=0.3
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": MOVIE_RAG_PROMPT},
        return_source_documents=True   
    )
    return chain