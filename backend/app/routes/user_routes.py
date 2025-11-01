from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.user_model import User, CheckHistory
from utils.helpers import get_current_user

router = APIRouter()

# Mock database (replace with actual database in production)
users_db = {}
history_db = {}


@router.post("/register")
async def register_user(user_data: dict):
    """Register a new user"""
    try:
        user_id = user_data.get("email") or user_data.get("phone")
        if not user_id:
            raise HTTPException(
                status_code=400, detail="Email or phone required")

        if user_id in users_db:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            id=user_id,
            email=user_data.get("email"),
            phone=user_data.get("phone"),
            name=user_data.get("name"),
            preferred_language=user_data.get("preferred_language", "en")
        )

        users_db[user_id] = user.dict()

        return {
            "status": "success",
            "user_id": user_id,
            "message": "User registered successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    return users_db[user_id]


@router.post("/history/{user_id}")
async def add_check_history(user_id: str, history_item: dict):
    """Add fact-check history for user"""
    try:
        if user_id not in history_db:
            history_db[user_id] = []

        history_entry = CheckHistory(
            id=len(history_db[user_id]) + 1,
            user_id=user_id,
            input_text=history_item.get("input_text", ""),
            input_type=history_item.get("input_type", "text"),
            result=history_item.get("result", {}),
            timestamp=history_item.get("timestamp")
        )

        history_db[user_id].append(history_entry.dict())

        return {"status": "success", "message": "History added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
async def get_user_history(user_id: str, limit: int = 10):
    """Get user's fact-check history"""
    if user_id not in history_db:
        return {"history": []}

    history = history_db[user_id][-limit:]
    return {
        "user_id": user_id,
        "history": history[::-1]  # Return in reverse chronological order
    }


@router.put("/preferences/{user_id}")
async def update_user_preferences(user_id: str, preferences: dict):
    """Update user preferences"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    users_db[user_id].update(preferences)
    return {"status": "success", "message": "Preferences updated"}
