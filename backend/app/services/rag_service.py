import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.core_utils.create_chunks import create_chunks
from app.core_utils.embedding_manager import embedding_manager
from app.core_utils.vector_store import vector_store
from app.core_utils.rag_retrieval import RAGRetrieval 

load_dotenv()

# Initialize Groq LLM
groq_api_key = os.getenv('GROQ_RAG_KEY')
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=1024
)

def generate_embedding_service():
    """Builds chunks, generates embeddings, and populates the vector store."""
    print("🔄 Running initial embedding generation service...")
    texts = []
    
    # Create chunks
    doc_chunks = create_chunks()
    for doc_chunk in doc_chunks:
        texts.append(doc_chunk.page_content)
        
    # Create embeddings
    embeddings = embedding_manager.generate_embeddings(texts=texts)
    
    # Add embeddings to vector store
    vector_store.adding_embeddings_to_store(chunks=doc_chunks, embeddings=embeddings)
    print("Embedding generation and vector store population complete.")


def query_rag_service(query: str, top_k: int = 3) -> str:
    """Retrieves relevant chunks and generates an answer using LLM."""
    retriever = RAGRetrieval(vector_store=vector_store, embedding_manager=embedding_manager)
    result = retriever.retrieve(query, topk_k=top_k)
    
    context = "\n\n".join([doc["document"] for doc in result]) if result else ""
    if not context:
        print("No relevant content found to answer the question")
        
    prompt = f"""Use the following context to answer the question concisely.
    Context: {context}
    Question: {query}
    
    Answer:"""
    
    # Pass prompt string directly to avoid formatting errors
    response = llm.invoke(prompt)
    return response.content