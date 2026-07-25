import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingManager:
    """In here each chunks or a text convert into embeddings
    """
    
    def __init__(self, model_name:str = "all-MiniLm-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """Load the SentenceTransformer model
        """
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded successfully. Embedding dimension: {self.model.get_embedding_dimension()}")
        except Exception as e:
            print(f"Can not load SentenceTransformer model. Error is: {e}")
            raise
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """generate the embedding for the chunks or text that have provided

        Args:
            texts (List[str]): get texts or chunks as argument

        Returns:
            np.ndarray: return numpy array
        """
        if not self.model:
            raise ValueError("Model is not loaded")
        
        print(f"Generating embedings for {len(texts)} texts...")
        embeddings = self.model.encode(texts,show_progress_bar=True)
        print(f"Generated embedding with shape {embeddings.shape}")
        return embeddings
    
embedding_manager = EmbeddingManager()