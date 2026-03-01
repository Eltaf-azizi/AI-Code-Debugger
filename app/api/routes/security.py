"""
Security Analysis Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_ai_service
from app.models.request_models import SecurityRequest
from app.models.response_models import SecurityResponse
from app.services.ai_service import AIService
from app.analyzers.security_scanner import scan_security

router = APIRouter()


@router.post("/security", response_model=SecurityResponse)
async def analyze_security(
    request: SecurityRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Analyze code security.
    
    Args:
        request: Security analysis request
        ai_service: AI service
    
    Returns:
        Security analysis results
    """
    try:
        language = request.language or "auto"
        
        # Get AI security analysis
        ai_result = ai_service.analyze_structured(
            code=request.code,
            action="security",
            language=language
        )
        
        # Get static security scan if requested
        static_results = {}
        if request.include_owasp:
            static_results = scan_security(request.code)
        
        # Combine results
        risks = ai_result.get("security_risks", [])
        
        # Add static scan findings
        if static_results.get("findings"):
            for finding in static_results["findings"]:
                risks.append({
                    "line": finding["line"],
                    "risk": finding["category"],
                    "severity": finding["severity"],
                    "fix": finding["suggestion"]
                })
        
        # Calculate risk score
        risk_score = 0
        severity_weights = {"Critical": 25, "High": 15, "Medium": 5, "Low": 1}
        for risk in risks:
            risk_score += severity_weights.get(risk.get("severity", "Low"), 1)
        risk_score = min(risk_score, 100)
        
        return SecurityResponse(
            success=True,
            security_risks=risks,
            risk_score=risk_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
