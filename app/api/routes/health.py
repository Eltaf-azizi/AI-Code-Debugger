"""
Health Check Routes
"""
from fastapi import APIRouter, Depends
from datetime import datetime

from app.config import settings
from app.models.response_models import HealthResponse

router = APIRouter()

# Track startup time
start_time = datetime.utcnow()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    uptime = (datetime.utcnow() - start_time).total_seconds()
    
    # Check configuration
    config_status = "configured" if settings.is_configured else "not configured"
    
    return HealthResponse(
        status="healthy" if settings.is_configured else "degraded",
        version=settings.APP_VERSION,
        uptime=uptime,
        checks={
            "configuration": config_status,
            "openai_api": "connected" if settings.is_configured else "disconnected"
        }
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns:
        Readiness status
    """
    return {
        "ready": settings.is_configured,
        "message": "API is ready" if settings.is_configured else "API not configured"
    }
