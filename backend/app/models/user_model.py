from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    preferred_language: str = "en"
    created_at: str = datetime.now().isoformat()
    
    class Config:
        schema_extra = {
            "example": {
                "id": "user@example.com",
                "email": "user@example.com",
                "name": "John Doe",
                "preferred_language": "en",
                "created_at": "2024-01-01T00:00:00"
            }
        }

class CheckHistory(BaseModel):
    id: int
    user_id: str
    input_text: str
    input_type: str  # text, voice, image
    result: Dict[str, Any]
    timestamp: str = datetime.now().isoformat()
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user@example.com",
                "input_text": "Sample news text...",
                "input_type": "text",
                "result": {"risk_level": "low", "confidence": 0.8},
                "timestamp": "2024-01-01T00:00:00"
            }
        }