"""
Optimize Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ai_service
from app.models.request_models import OptimizeRequest
from app.models.response_models import OptimizeResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_code(
    request: OptimizeRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Optimize code.
    
    Args:
        request: Optimization request
        ai_service: AI service
    
    Returns:
        Optimization results
    """
    try:
        language = request.language or "auto"
        
        # Add focus context
        context = ""
        if request.focus == "performance":
            context = "Focus on performance optimizations."
        elif request.focus == "memory":
            context = "Focus on memory efficiency."
        
        # Get structured response
        result = ai_service.analyze_structured(
            code=request.code,
            action="optimize",
            language=language
        )
        
        # Handle error
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return OptimizeResponse(
            success=True,
            performance_suggestions=result.get("performance_suggestions", []),
            refactor_suggestions=result.get("refactor_suggestions", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
