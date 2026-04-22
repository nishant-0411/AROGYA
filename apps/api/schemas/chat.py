"""
Chat Schemas

Pydantic models for chat request and response.
"""

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    patient_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
