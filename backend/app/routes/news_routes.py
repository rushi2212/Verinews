from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
import json
from ..services.ai_analyzer import NewsAnalyzer
from ..services.speech_processor import SpeechProcessor
from ..services.fact_checker import FactChecker
from ..services.retrieval_verifier import verify_with_osint
import asyncio

router = APIRouter()
news_analyzer = NewsAnalyzer()
speech_processor = SpeechProcessor()
fact_checker = FactChecker()


@router.post("/check-text")
async def check_news_text(text: str = Form(...), language: str = Form("en")):
    """Analyze text news for authenticity"""
    try:
        # Analyze the news content
        analysis = news_analyzer.analyze_text(text, language)

        # Fact check against known sources
        fact_check = await fact_checker.verify_claims(text)

        # Retrieval-augmented verification (Tavily + Gemini)
        verification = await asyncio.to_thread(verify_with_osint, text)

        # Prefer calibrated verification confidence when available
        overall_conf = analysis.get("confidence_score", 0.5)
        if isinstance(verification, dict) and verification.get("status") == "ok":
            overall_conf = float(verification.get("confidence", overall_conf))

        return {
            "status": "success",
            "analysis": analysis,
            "fact_check": fact_check,
            "verification": verification,
            "confidence_score": overall_conf
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-voice")
async def check_news_voice(audio_file: UploadFile = File(...), language: str = Form("en")):
    """Process voice input and check news"""
    try:
        # Convert speech to text
        text = await speech_processor.speech_to_text(audio_file, language)

        # Analyze the converted text
        analysis = news_analyzer.analyze_text(text, language)
        fact_check = await fact_checker.verify_claims(text)
        verification = await asyncio.to_thread(verify_with_osint, text)

        overall_conf = analysis.get("confidence_score", 0.5)
        if isinstance(verification, dict) and verification.get("status") == "ok":
            overall_conf = float(verification.get("confidence", overall_conf))

        return {
            "status": "success",
            "original_text": text,
            "analysis": analysis,
            "fact_check": fact_check,
            "verification": verification,
            "confidence_score": overall_conf
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-image")
async def check_news_image(
    image_file: UploadFile = File(...),
    text: Optional[str] = Form(None),
    language: str = Form("en")
):
    """Analyze image with potential fake news"""
    try:
        # Extract text from image using OCR
        extracted_text = await news_analyzer.extract_text_from_image(image_file)

        # Combine with provided text
        full_text = f"{text or ''} {extracted_text}".strip()

        analysis = news_analyzer.analyze_text(full_text, language)
        fact_check = await fact_checker.verify_claims(full_text)
        verification = await asyncio.to_thread(verify_with_osint, full_text)

        overall_conf = analysis.get("confidence_score", 0.5)
        if isinstance(verification, dict) and verification.get("status") == "ok":
            overall_conf = float(verification.get("confidence", overall_conf))

        return {
            "status": "success",
            "extracted_text": extracted_text,
            "analysis": analysis,
            "fact_check": fact_check,
            "verification": verification,
            "confidence_score": overall_conf
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
async def get_check_history(user_id: str):
    """Get user's fact-check history"""
    # Implementation for history retrieval
    return {"user_id": user_id, "history": []}
