import os
from qdrant_client import QdrantClient
from apps.worker.queues.celery_app import celery_app
from src.arogya.multimodal.pdf_pipeline import process_pdf
from src.arogya.multimodal.text_pipeline import process_text
from src.arogya.rag.chunking import chunk_text
from src.arogya.rag.embeddings import get_embedding_model
from src.arogya.rag.retriever import create_vectorstore, add_documnents

@celery_app.task(name="apps.worker.jobs.ingest_documents")
def ingest_document_task(file_path: str, file_type: str):
    if file_type == "pdf":
        result = process_pdf(file_path)
    elif file_type == "text":
        result = process_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
        
    text = result["content"]
    metadata = result.get("metadata", {})
    
    chunks = chunk_text(text)
    
    metadata_list = [metadata.copy() for _ in chunks]
    
    qdrant_url = os.environ.get("QDRANT_URL")
    if qdrant_url:
        client = QdrantClient(url=qdrant_url)
    else:
        qdrant_path = os.environ.get("QDRANT_PATH", "local_qdrant")
        client = QdrantClient(path=qdrant_path)
    
    embeddings = get_embedding_model()
    
    vectorstore = create_vectorstore(client, "arogya_docs", embeddings)
    
    add_documnents(vectorstore, chunks, metadata_list)
    
    return {"status": "success", "chunks_processed": len(chunks)}
