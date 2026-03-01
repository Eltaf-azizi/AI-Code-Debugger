"""
Explain Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ai_service
from app.models.request_models import ExplainRequest
from app.models.response_models import ExplainResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def explain_code(
    request: ExplainRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Explain code.
    
    Args:
        request: Explanation request
        ai_service: AI service
    
    Returns:
        Code explanation
    """
    try:
        language = request.language or "auto"
        
        # Add detail level context
        context = ""
        if request.detail_level == "brief":
            context = "Provide a brief explanation."
        elif request.detail_level == "detailed":
            context = "Provide a detailed explanation with examples."
        
        # Get analysis
        result = ai_service.analyze(
            code=request.code,
            action="explain",
            language=language,
            additional_context=context
        )
        
        return ExplainResponse(
            success=True,
            overview=result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
