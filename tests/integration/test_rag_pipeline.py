"""
Integration Test for RAG Pipeline

Tests the full RAG workflow including chunking, embedding generation,
and Qdrant vector retrieval.
"""

from qdrant_client import QdrantClient
from src.arogya.rag.chunking import chunk_text
from src.arogya.rag.embeddings import get_embedding_model
from src.arogya.rag.retriever import create_vectorstore, add_documnents, gen_retriever

def test_rag_pipeline_end_to_end():
    print("Testing the RAG Pipeline (End-to-End)...")
    
    # 1. Sample Data
    sample_text = (
        "Type 2 diabetes is a chronic condition that affects the way the body processes blood sugar (glucose). "
        "Symptoms include increased thirst, frequent urination, hunger, fatigue, and blurred vision. "
        "Treatment often involves a combination of lifestyle changes, such as diet and exercise, and medications "
        "like Metformin or insulin therapy."
    )
    
    chunks = chunk_text(sample_text)
    assert len(chunks) > 0, "Chunking should return at least one text chunk."
    
    embedding_model = get_embedding_model()
    assert embedding_model is not None, "Embedding model should be initialized."
    
    client = QdrantClient(":memory:")
    collection_name = "test_medical_rag"
    
    from qdrant_client.models import Distance, VectorParams
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    
    vectorstore = create_vectorstore(
        client=client,
        collection_name=collection_name,
        embeddings=embedding_model
    )
    
    add_documnents(
        vectorstore=vectorstore,
        texts=chunks,
        metadata_list=[{"source": "test_medical_text"} for _ in chunks]
    )
    
    retriever = gen_retriever(vectorstore)
    
    query = "What is the common treatment for Type 2 diabetes?"
    retrieved_docs = retriever.invoke(query)
    
    assert len(retrieved_docs) > 0, "Retriever should find relevant documents."

    assert any("Treatment" in doc.page_content or "Metformin" in doc.page_content for doc in retrieved_docs), "Retrieved docs should contain relevant context."
    assert retrieved_docs[0].metadata.get("source") == "test_medical_text", "Metadata should be preserved."

