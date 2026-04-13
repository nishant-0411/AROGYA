"""
Unit tests for the chunking logic in the Arogya application.
Tests that the LangChain RecursiveCharacterTextSplitter returns correct chunk sizes.
"""

from src.arogya.rag.chunking import chunk_text

def test_chunk_text():
    sample_text = "A" * 600
    
    chunks = chunk_text(sample_text)
    
    assert len(chunks) == 2
    
    assert len(chunks[0]) <= 500
    assert len(chunks[1]) <= 500
    
    assert "A" in chunks[0]
