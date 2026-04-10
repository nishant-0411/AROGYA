# Test PDF extraction
from src.arogya.multimodal.pdf_pipeline import process_pdf

def test_pdf():
    result = process_pdf("sample.pdf")
    assert "content" in result
    assert "metadata" in result

