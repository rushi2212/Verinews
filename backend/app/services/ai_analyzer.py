import re
import json
from typing import Dict, List
import io
import base64
import logging
from urllib import request, error
from utils.config import settings

logger = logging.getLogger(__name__)


class NewsAnalyzer:
    def __init__(self):
        # Rule-based analysis (no heavy ML dependencies required)
        self.sentiment_analyzer = None
        self.fake_news_detector = None
        self.reader = None

    def analyze_text(self, text: str, language: str = "en") -> Dict:
        """Analyze text for fake news indicators using rule-based approach"""

        # Basic text analysis
        text_metrics = self._calculate_text_metrics(text)

        # Rule-based sentiment analysis (no ML needed)
        sentiment = self._analyze_sentiment_rules(text)

        # Rule-based fake news detection
        fake_news_score = self._detect_fake_news_rules(text)

        # Linguistic analysis
        linguistic_features = self._analyze_linguistic_features(text)

        return {
            "text_metrics": text_metrics,
            "sentiment": sentiment,
            "fake_news_probability": fake_news_score,
            "linguistic_features": linguistic_features,
            "confidence_score": self._calculate_confidence(text_metrics, linguistic_features),
            "risk_level": self._determine_risk_level(text)
        }

    def _analyze_sentiment_rules(self, text: str) -> Dict:
        """Detect sentiment using keyword-based rules"""
        text_lower = text.lower()

        positive_words = ['good', 'great', 'excellent', 'amazing',
                          'wonderful', 'positive', 'success', 'strong', 'growth']
        negative_words = ['bad', 'terrible', 'horrible', 'awful',
                          'disaster', 'crisis', 'failure', 'collapse', 'death']

        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            return {"label": "POSITIVE", "score": min(0.95, 0.5 + pos_count * 0.1)}
        elif neg_count > pos_count:
            return {"label": "NEGATIVE", "score": min(0.95, 0.5 + neg_count * 0.1)}
        else:
            return {"label": "NEUTRAL", "score": 0.5}

    def _detect_fake_news_rules(self, text: str) -> float:
        """Detect fake news probability using rule-based patterns"""
        text_lower = text.lower()
        score = 0.3  # baseline

        # Check for sensationalism
        sensational_words = ['shocking', 'unbelievable', 'you won\'t believe',
                             'they don\'t want', 'secret revealed', 'exclusive']
        sensational_count = sum(
            1 for word in sensational_words if word in text_lower)
        score += sensational_count * 0.15

        # Check for vague language
        vague_phrases = ['some people say', 'experts claim',
                         'allegedly', 'reportedly', 'rumor has it']
        vague_count = sum(
            1 for phrase in vague_phrases if phrase in text_lower)
        score += vague_count * 0.1

        # Check for emotional appeals
        emotional_words = ['outrageous', 'disgusting',
                           'evil', 'conspiracy', 'cover-up', 'corruption']
        emotional_count = sum(
            1 for word in emotional_words if word in text_lower)
        score += emotional_count * 0.12

        # Check for credible sources
        credible_sources = ['reuters', 'ap news', 'bbc',
                            'associated press', 'government', 'official', 'study', 'research']
        credible_count = sum(
            1 for source in credible_sources if source in text_lower)
        score -= credible_count * 0.1

        # Check for numbers and dates (typically more credible)
        numbers = len(re.findall(r'\d+', text))
        score -= min(0.15, numbers * 0.05)

        return max(0.0, min(1.0, score))

    def _calculate_text_metrics(self, text: str) -> Dict:
        """Calculate various text metrics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)

        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_sentence_length": len(words) / max(len([s for s in sentences if s.strip()]), 1),
            "capital_ratio": sum(1 for c in text if c.isupper()) / max(len(text), 1),
            "exclamation_count": text.count('!'),
            "question_count": text.count('?')
        }

    def _analyze_linguistic_features(self, text: str) -> Dict:
        """Analyze linguistic patterns associated with fake news"""
        # Common fake news indicators
        urgency_words = ['urgent', 'breaking', 'shocking', 'alert', 'warning']
        emotional_words = ['outrageous', 'unbelievable', 'amazing', 'terrible']
        vague_words = ['they', 'them', 'some people', 'experts say']

        text_lower = text.lower()

        return {
            "urgency_score": sum(text_lower.count(word) for word in urgency_words),
            "emotional_score": sum(text_lower.count(word) for word in emotional_words),
            "vague_references": sum(text_lower.count(word) for word in vague_words),
            "has_clickbait": any(word in text_lower for word in urgency_words[:3])
        }

    def _calculate_confidence(self, text_metrics: Dict, linguistic_features: Dict) -> float:
        """Calculate confidence score for analysis"""
        base_score = 0.7

        # Adjust based on text quality
        if text_metrics['word_count'] < 10:
            base_score -= 0.3
        elif text_metrics['word_count'] > 50:
            base_score += 0.1

        # Adjust based on linguistic features
        if linguistic_features['urgency_score'] > 3:
            base_score -= 0.2
        if linguistic_features['emotional_score'] > 5:
            base_score -= 0.1

        return max(0.1, min(0.95, base_score))

    def _determine_risk_level(self, text: str) -> str:
        """Determine risk level of content"""
        risk_keywords = {
            'high': ['death', 'kill', 'emergency', 'danger', 'warning'],
            'medium': ['fake', 'hoax', 'scam', 'fraud'],
            'low': ['maybe', 'possibly', 'rumor']
        }

        text_lower = text.lower()
        high_count = sum(text_lower.count(word)
                         for word in risk_keywords['high'])
        medium_count = sum(text_lower.count(word)
                           for word in risk_keywords['medium'])

        if high_count > 0:
            return "high"
        elif medium_count > 2:
            return "medium"
        else:
            return "low"

    async def extract_text_from_image(self, image_file) -> str:
        """Extract text from image using OCR. If easyocr/Pillow aren't installed,
        return an empty string to keep the API runnable."""
        image_data = await image_file.read()
        mime_type = getattr(image_file, 'content_type',
                            'image/png') or 'image/png'

        try:
            from PIL import Image
            import easyocr
            import numpy as np

            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            image_np = np.array(image)

            if self.reader is None:
                self.reader = easyocr.Reader(['en', 'hi', 'ta', 'te', 'bn'])

            results = self.reader.readtext(image_np)
            extracted_text = ' '.join([result[1] for result in results])
            return extracted_text
        except Exception:
            # Fallback: Use Gemini multimodal to OCR without local deps
            try:
                return self._ocr_with_gemini(image_data, mime_type)
            except Exception:
                return ""

    def _ocr_with_gemini(self, image_bytes: bytes, mime_type: str) -> str:
        api_key = settings.GOOGLE_API_KEY
        preferred = settings.GEMINI_MODEL or "gemini-2.5-flash"
        # try a set of common multimodal-capable variants
        candidates = [
            preferred,
            "gemini-2.5-flash-001",
            "gemini-2.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-latest",
        ]
        if not api_key:
            return ""

        b64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": "Extract all readable text present in this image. Return only raw text, with newlines between blocks. Do not add explanations."},
                        {"inlineData": {"mimeType": mime_type, "data": b64}},
                    ],
                }
            ]
        }

        for model in candidates:
            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
            data = json.dumps(payload).encode('utf-8')
            req = request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with request.urlopen(req, timeout=30.0) as resp:
                    body = resp.read().decode('utf-8')
                    res = json.loads(body)
                    text = ""
                    try:
                        candidates_out = res.get("candidates") or []
                        if candidates_out:
                            content = candidates_out[0].get("content") or {}
                            parts = content.get("parts") or []
                            # concatenate all text parts for OCR output
                            for p in parts:
                                if "text" in p:
                                    text += (p.get("text") or "") + "\n"
                    except Exception:
                        text = ""
                    if text.strip():
                        return text.strip()
            except error.HTTPError as e:
                try:
                    detail = e.read().decode('utf-8', errors='ignore')
                except Exception:
                    detail = ""
                logger.warning("Gemini OCR HTTPError %s on %s: %s",
                               e.code, model, detail[:200])
                continue
            except Exception as e:
                logger.warning("Gemini OCR failed on %s: %s", model, e)
                continue

        return ""
