"""This script enables the generation and ingestion of sample demo data for the application."""

import os
from src.arogya.multimodal.pdf_pipeline import process_pdf
from src.arogya.multimodal.image_pipeline import process_image
from src.arogya.multimodal.text_pipeline import process_text

def seed():
    print("Seeding demo data using Langchain pipelines...")
    
    sample_txt = "demo_sample.txt"
    with open(sample_txt, "w") as f:
        f.write("This is sample text data for AROGYA.")
        
    try:
        result = process_text(sample_txt)
        print(f"Processed Text Data: {result}")
    finally:
        if os.path.exists(sample_txt):
            os.remove(sample_txt)

if __name__ == "__main__":
    seed()