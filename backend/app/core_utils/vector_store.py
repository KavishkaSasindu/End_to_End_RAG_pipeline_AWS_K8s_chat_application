import chromadb
import os
from typing import List,Any
import numpy as np
import uuid

class VectorStore:
    """Create vector store and adding embeddings to vector store
    """
    
    def __init__(self, collection_name:str = "pdf_documents", persist_directory:str = "./data/vector_store"):
        self.collection_name =collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()
        
    def _initialize_store(self):
        """Initialize the chromadb client"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory
            )
            os.makedirs(self.persist_directory,exist_ok=True)
            self.collection = self.client.get_or_create_collection(
                name = self.collection_name,
                metadata = {
                    "description":"PDF document embeddings RAG",
                    "hnsw:space":"cosine"
                }
            )
            print(f"Vector store initialized. Collection {self.collection_name}")
            print(f"Existing document in collection: {self.collection.count()}")
        except Exception as e:
            print(f"Error initialize vector store. Error is: {e}")
            raise
        
    def adding_embeddings_to_store(self, chunks: List[Any],embeddings: np.ndarray):
        """Add documents and their embedding to vector store ChromaDB

        Args:
            chunks (List[Any]): List of chunks for each langchain documents
            embeddings (np.ndarray): Corresponding embeddings for the documents
        """        
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must be matched with the number of embeddings")
        
        print(f"Adding {len(chunks)} chunks to the vector store")
        
        # prepare data for chromodb
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i,(doc,embedding) in enumerate(zip(chunks,embeddings)):
            #generate unique id
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            # prepare for metadata
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            
            # Docmuent content
            documents_text.append(doc.page_content)
            
            # Embedding
            embeddings_list.append(embedding.tolist())
            
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                metadatas=metadatas,
                embeddings=embeddings_list,
                documents=documents_text
            )
            
            print(f"Successfully added {len(chunks)} documents to vector store")
            print(f"Total documents in collection: {self.collection.count()}")
        except Exception as e:
            print(f"Can not add to collection data to chromadb error is : {e}")
            raise

vector_store = VectorStore()