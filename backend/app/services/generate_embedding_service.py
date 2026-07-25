from app.core_utils import create_chunks
from app.core_utils.embedding_manager import embedding_manager
from app.core_utils.vector_store import vector_store

def generate_embedding_service():
    texts = []
    
    if not doc_chunks:
        print("⚠️ No PDFs found or no chunks created. Skipping vector store population.")
        return
    
    # create chunk and store in array
    doc_chunks = create_chunks()
    for doc_chunk in doc_chunks:
        texts.append(doc_chunk.page_content)
        
    # create embedding with above doc_chunks
    embeddings = embedding_manager.generate_embeddings(texts=texts)
    
    # add embeddings to vector store
    vector_store.adding_embeddings_to_store(chunks=doc_chunks,embeddings=embeddings)
    
    