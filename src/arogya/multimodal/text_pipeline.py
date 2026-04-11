"""This module provides functionality to load and process raw text files using Langchain's TextLoader."""
from typing import Dict
from langchain_community.document_loaders import TextLoader

def process_text(file_path: str) -> Dict:
    loader = TextLoader(file_path)
    docs = loader.load()
    
    text = "\n".join([doc.page_content for doc in docs])
    
    return {
        "type": "text",
        "content": text.strip(),
        "metadata": {
            "source": file_path
        }
    }