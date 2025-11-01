from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class NewsAnalysisRequest(BaseModel):
    text: str
    language: str = "en"
    input_type: str = "text"

class VoiceAnalysisRequest(BaseModel):
    audio_data: str  # base64 encoded audio
    language: str = "en"

class ImageAnalysisRequest(BaseModel):
    image_data: str  # base64 encoded image
    text: Optional[str] = None
    language: str = "en"

class AnalysisResponse(BaseModel):
    status: str
    analysis: Dict[str, Any]
    fact_check: Dict[str, Any]
    confidence_score: float
    risk_level: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "analysis": {
                    "fake_news_probability": 0.15,
                    "sentiment": {"label": "POSITIVE", "score": 0.8},
                    "risk_level": "low"
                },
                "fact_check": {
                    "claims_found": 2,
                    "overall_credibility": 0.9
                },
                "confidence_score": 0.85,
                "risk_level": "low"
            }
        }