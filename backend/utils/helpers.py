import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from .config import settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(token: str):
    """Get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    return payload

def format_timestamp(timestamp: str = None) -> str:
    """Format timestamp for consistent display"""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    return timestamp

def calculate_reading_time(text: str) -> int:
    """Calculate estimated reading time in seconds"""
    words_per_minute = 200
    word_count = len(text.split())
    reading_time_minutes = word_count / words_per_minute
    return max(1, int(reading_time_minutes * 60))