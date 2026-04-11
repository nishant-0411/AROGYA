"""
This module defines the response schemas for the file upload API endpoints using Pydantic.
"""

from pydantic import BaseModel
from typing import Dict, Any

class UploadResponse(BaseModel):
    type: str
    content: str
    metadata: Dict[str, Any]