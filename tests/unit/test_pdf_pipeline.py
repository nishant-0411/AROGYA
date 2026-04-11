"""
This module contains unit tests for the PDF ingestion pipeline. 
It verifies that the Langchain-based PyPDFLoader correctly processes a document,
extracts its text content, and returns the expected dictionary structure with 
the 'type', 'content', and 'metadata' keys, conforming to the system's baseline.
"""

from unittest.mock import patch, MagicMock
from src.arogya.multimodal.pdf_pipeline import process_pdf

@patch("src.arogya.multimodal.pdf_pipeline.PyPDFLoader")
def test_pdf(mock_pypdf_loader_class):
    mock_document = MagicMock()
    mock_document.page_content = "This is a test PDF content."
    mock_document.metadata = {"page": 0, "source": "sample.pdf"}
    
    mock_loader_instance = MagicMock()
    mock_loader_instance.load.return_value = [mock_document]
    mock_pypdf_loader_class.return_value = mock_loader_instance

    result = process_pdf("sample.pdf")
    
    assert result["type"] == "pdf"
    assert result["content"] == "This is a test PDF content."
    assert "metadata" in result
    assert result["metadata"]["source"] == "sample.pdf"
    assert result["metadata"]["total_pages"] == 1
