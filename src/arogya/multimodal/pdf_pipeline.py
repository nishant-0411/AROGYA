# Extract text from PDFs and convert into structured document format
from typing import Dict

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    try:
        from PyPDF2 import PdfReader
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "PDF support requires 'pypdf' or 'PyPDF2'. Install project "
            "dependencies before processing PDFs."
        ) from exc


def process_pdf(file_path: str) -> Dict:
    text = ""
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""

    return {
        "type": "pdf",
        "content": text,
        "metadata": {"source": file_path}
    }
