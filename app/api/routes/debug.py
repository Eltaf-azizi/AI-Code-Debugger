"""
Debug Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ai_service
from app.models.request_models import DebugRequest
from app.models.response_models import DebugResponse
from app.services.ai_service import AIService
from app.analyzers import python_analyzer

router = APIRouter()


@router.post("/debug", response_model=DebugResponse)
async def debug_code(
    request: DebugRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Debug code.
    
    Args:
        request: Debug request
        ai_service: AI service
    
    Returns:
        Debug results
    """
    try:
        language = request.language or "auto"
        
        # Get AI analysis
        result = ai_service.analyze_structured(
            code=request.code,
            action="debug",
            language=language
        )
        
        # Handle error
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Get static analysis if requested
        static_errors = []
        if request.include_static_analysis and language in ("python", "auto"):
            static = python_analyzer.analyze_python(request.code)
            if "syntax_error" in static:
                static_errors.append(static["syntax_error"])
        
        return DebugResponse(
            success=True,
            syntax_errors=result.get("syntax_errors", static_errors),
            logical_issues=result.get("logical_issues", []),
            corrected_code=result.get("corrected_code")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
