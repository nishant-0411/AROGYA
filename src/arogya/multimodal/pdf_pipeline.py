"""This module provides functionality to extract text from PDF files using Langchain's PyPDFLoader."""
from typing import Dict
from langchain_community.document_loaders import PyPDFLoader

def process_pdf(file_path: str) -> Dict:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text = "\n".join([doc.page_content for doc in docs])
    
    return {
        "type": "pdf",
        "content": text,
        "metadata": {
            "source": file_path,
            "total_pages": len(docs)
        }
    }
