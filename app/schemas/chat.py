from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    message: str


class KBReference(BaseModel):
    id: str
    title: str


class ChatResponse(BaseModel):
    answer: str
    kbReferences: List[KBReference]
    confidence: float
    tier: str
    severity: str
    needsEscalation: bool
