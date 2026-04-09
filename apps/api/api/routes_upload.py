# API endpoint to upload and route files
from fastapi import APIRouter, UploadFile
from src.arogya.multimodal.pdf_pipeline import process_pdf
from src.arogya.multimodal.image_pipeline import process_image
from src.arogya.multimodal.text_pipeline import process_text

router = APIRouter()

async def upload_files(file: UploadFile):
    file_path = f"temp_{file.filename}"

    with open(file_path, 'wb') as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        return process_pdf(file_path)
    
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        return process_image(file_path)
    
    elif file.filename.endswith(".txt"):
        with open(file_path, "r") as f:
            return process_text(f.read())
    
    return {"error": "Unsupported file type"}