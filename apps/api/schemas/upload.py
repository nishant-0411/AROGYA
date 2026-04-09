# Define response structure
from pydantic import BaseModel
from typing import Dict

class UploadResponse(BaseModel):
    type: str
    content: str
    metadata: Dict