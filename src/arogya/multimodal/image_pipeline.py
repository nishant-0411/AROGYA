#Extract text (OCR) from images

from PIL import Image
import pytesseract

def process_image(file_path: str)-> dict:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)

    return {
        "type": "image",
        "content": text,
        "metadata": {
            "source": file_path
        }
    }