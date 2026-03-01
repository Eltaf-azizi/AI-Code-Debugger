"""
Improvement Service
Code optimization and refactoring
"""
from typing import Dict, Any, Optional

from app.services.ai_service import AIService
from app.services.prompt_templates import detect_language


class ImprovementService:
    """
    Service for code improvement.
    Handles optimization and refactoring suggestions.
    """
    
    def __init__(self, ai_service: AIService):
        """Initialize with AI service."""
        self.ai_service = ai_service
    
    def optimize(
        self,
        code: str,
        language: Optional[str] = None,
        structured: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize the given code for better performance.
        
        Args:
            code: Source code to optimize
            language: Programming language
            structured: Whether to return structured JSON
            
        Returns:
            Optimization suggestions and improved code
        """
        if language is None or language == "auto":
            language = detect_language(code)
        
        if structured:
            return self.ai_service.analyze_structured(code, "optimize", language)
        else:
            result = self.ai_service.analyze(code, "optimize", language)
            return {"optimization": result}
    
    def refactor(
        self,
        code: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refactor the given code for better structure.
        
        Args:
            code: Source code to refactor
            language: Programming language
            
        Returns:
            Refactored code and suggestions
        """
        if language is None or language == "auto":
            language = detect_language(code)
        
        result = self.ai_service.analyze(code, "refactor", language)
        return {"refactoring": result}
    
    def get_performance_suggestions(
        self,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Get performance improvement suggestions.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Performance suggestions
        """
        return self.ai_service.analyze_structured(code, "optimize", language)
