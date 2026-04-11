"""
This API module defines the file upload endpoints for the application using FastAPI.
It handles incoming multimodal files (PDFs, images, and text), saves them temporarily to disk, 
routes each file to its corresponding Langchain-powered processing pipeline, and returns 
a standardized JSON format with the extracted content and metadata.
"""

import os
from fastapi import APIRouter, UploadFile, HTTPException
from src.arogya.multimodal.pdf_pipeline import process_pdf
from src.arogya.multimodal.image_pipeline import process_image
from src.arogya.multimodal.text_pipeline import process_text

router = APIRouter()

@router.post("/upload")
async def upload_files(file: UploadFile):
    file_path = f"temp_{file.filename}"

    with open(file_path, 'wb') as f:
        f.write(await file.read())

    try:
        if file.filename.endswith(".pdf"):
            result = process_pdf(file_path)
        
        elif file.filename.endswith((".png", ".jpg", ".jpeg")):
            result = process_image(file_path)
        
        elif file.filename.endswith(".txt"):
            result = process_text(file_path)
            
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return result
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)