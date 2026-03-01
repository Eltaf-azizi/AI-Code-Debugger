"""
Debugger Service
AI-powered code debugging
"""
from typing import Dict, Any, List, Optional

from app.services.ai_service import AIService
from app.services.prompt_templates import detect_language
from app.analyzers import python_analyzer, error_parser


class DebuggerService:
    """
    Service for debugging code.
    Combines AI analysis with static analysis tools.
    """
    
    def __init__(self, ai_service: AIService):
        """Initialize with AI service."""
        self.ai_service = ai_service
    
    def debug(
        self,
        code: str,
        language: Optional[str] = None,
        structured: bool = True
    ) -> Dict[str, Any]:
        """
        Debug the given code.
        
        Args:
            code: Source code to debug
            language: Programming language
            structured: Whether to return structured JSON
            
        Returns:
            Debugging result with issues and fixes
        """
        if language is None or language == "auto":
            language = detect_language(code)
        
        # First, try static analysis for syntax errors
        static_results = self._run_static_analysis(code, language)
        
        # Then, use AI for deeper analysis
        if structured:
            ai_results = self.ai_service.analyze_structured(code, "debug", language)
        else:
            ai_results = {"analysis": self.ai_service.analyze(code, "debug", language)}
        
        # Combine results
        return {
            "static_analysis": static_results,
            "ai_analysis": ai_results,
            "language": language
        }
    
    def find_bugs(
        self,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Find bugs in code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Bug analysis result
        """
        return self.ai_service.analyze_structured(code, "debug", language)
    
    def suggest_fixes(
        self,
        code: str,
        language: str = "python"
    ) -> str:
        """
        Suggest fixes for code issues.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Fixed code
        """
        result = self.ai_service.analyze(code, "debug", language)
        
        # Extract corrected code from result
        # This is a simple implementation - could be enhanced
        return result
    
    def _run_static_analysis(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Run static analysis on code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Static analysis results
        """
        results = {
            "syntax_errors": [],
            "warnings": []
        }
        
        if language == "python":
            # Use Python's built-in parser
            errors = error_parser.parse_python_errors(code)
            results["syntax_errors"] = errors
        
        # Add more language-specific static analysis as needed
        
        return results
