"""
Script to create the necessary Qdrant collections for the Arogya application.
This leverages the Qdrant client to set up the collection which will store 
document embeddings created via LangChain's HuggingFaceEmbeddings.
"""

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os

QDRANT_PATH = os.path.join(os.path.dirname(__file__), "..", "local_qdrant")

def main():
    print(f"Initializing Qdrant client at {QDRANT_PATH}...")
    client = QdrantClient(path=QDRANT_PATH)
    
    collection_name = "arogya_docs"
    
    # all-MiniLM-L6-v2 produces 384 dimensional embeddings.
    # We define the VectorParams such that Qdrant is prepared to store these embeddings.
    vector_size = 384 
    
    print(f"Creating collection '{collection_name}'...")
    
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    
    print(f"Collection '{collection_name}' created successfully.")

if __name__ == "__main__":
    main()
