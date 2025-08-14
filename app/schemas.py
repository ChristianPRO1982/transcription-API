"""
Pydantic schemas for requests and responses.
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class TranscriptionResult(BaseModel):
    text: str
    language: str
    duration_sec: float
