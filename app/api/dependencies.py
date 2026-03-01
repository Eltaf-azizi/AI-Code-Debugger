"""
API Dependencies
Common dependencies for API routes
"""
from fastapi import Depends, HTTPException, status
from typing import Optional

from app.config import settings
from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    """
    Get AI service instance.
    
    Returns:
        AIService instance
    """
    if not settings.is_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please set OPENAI_API_KEY."
        )
    return AIService()


async def verify_api_key(api_key: Optional[str] = None) -> str:
    """
    Verify API key if required.
    
    Args:
        api_key: Optional API key from request
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    if settings.SECRET_KEY and api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key or ""
