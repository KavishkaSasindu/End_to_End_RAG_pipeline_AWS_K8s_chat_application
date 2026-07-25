from app.core_utils.vector_store import vector_store 
from app.core_utils.embedding_manager import EmbeddingManager,embedding_manager
from typing import List,Any,Dict

class RAGRetrieval:
    """Handle query based retrieval from vector store"""
    
    def __init__(self, vector_store, embedding_manager: EmbeddingManager):
        """Initialize retreiver

        Args:
            vectore_store (_type_): take vector store containing document embeddings
            embedding_manager (EmbeddingManager): create vector embeddings
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
        
    ## retrive function
    def retrieve(self, query: str, topk_k: int = 5, score_treshold: float =0.0) -> List[Dict[str, Any]]:
        """retrive based on query

        Args:
            query (str): user query
            topk_k (int, optional): retrive top 5 vectore embedding based on query from vector store. Defaults to 5.
            score_treshold (float, optional): _description_. Defaults to 0.0.

        Returns:
            List[Dict[str, Any]]: return value list of documents and metadata
        """
        print(f"Retreiving documents for query: '{query}'")
        print(f"Top K: {topk_k}, score treshold: {score_treshold}")
        
        #generate query embedding
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        
        # search in vector tore
        try:
            result = self.vector_store.collection.query(
                query_embeddings = [query_embedding.tolist()],
                n_results = topk_k
            )
            
            #process results
            retreived_docs = []
            
            if result['documents'] and result['documents'][0]:
                documents = result['documents'][0]
                metadatas = result['metadatas'][0]
                distances = result['distances'][0]
                ids = result['ids'][0]
                
                for i, (doc_id,document,metadata,distance) in enumerate(zip(ids,documents,metadatas,distances)):
                    #convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity_score = 1 - distance
                    
                    if similarity_score >=score_treshold:
                        retreived_docs.append({
                            'id': doc_id,
                            'document': document,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'rank': i +1
                        })
                print(f"Retrived {len(retreived_docs)} documents (after filtering)")
            else:
                print("No documents found")
            
            return retreived_docs
        
        except Exception as e:
            print(f"Can not search by query")
            return []
        
rag_retrieval = RAGRetrieval(vector_store=vector_store,embedding_manager=embedding_manager)