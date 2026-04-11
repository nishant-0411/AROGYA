"""This module provides functionality to extract text from image files using Langchain's 
UnstructuredImageLoader."""

from typing import Dict
from langchain_community.document_loaders.image import UnstructuredImageLoader

def process_image(file_path: str) -> Dict:
    loader = UnstructuredImageLoader(file_path)
    docs = loader.load()
    
    text = "\n".join([doc.page_content for doc in docs])
    
    return {
        "type": "image",
        "content": text,
        "metadata": {
            "source": file_path
        }
    }