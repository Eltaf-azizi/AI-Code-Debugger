"""
Summarize Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ai_service
from app.models.request_models import SummarizeRequest
from app.models.response_models import SummarizeResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_code(
    request: SummarizeRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Summarize code.
    
    Args:
        request: Summarization request
        ai_service: AI service
    
    Returns:
        Code summary
    """
    try:
        # Get language
        language = request.language or "auto"
        
        # Get structured response
        result = ai_service.analyze_structured(
            code=request.code,
            action="summarize",
            language=language
        )
        
        # Handle error
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return SummarizeResponse(
            success=True,
            file_summary=result.get("file_summary", ""),
            functions=result.get("functions", []),
            classes=result.get("classes", []),
            complexity_level=result.get("complexity_level", "Unknown")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
