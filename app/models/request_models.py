"""
Request Models
Pydantic models for API requests
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class AnalyzeCodeRequest(BaseModel):
    """Base request model for code analysis."""
    code: str = Field(..., description="Source code to analyze")
    language: Optional[str] = Field(None, description="Programming language (auto-detected if not specified)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def hello():\n    print('Hello, World!')",
                "language": "python"
            }
        }


class SummarizeRequest(AnalyzeCodeRequest):
    """Request model for code summarization."""
    structured(True, description=": bool = FieldReturn structured JSON response")


class DebugRequest(AnalyzeCodeRequest):
    """Request model for debugging."""
    include_static_analysis: bool = Field(True, description="Include static analysis results")


class ExplainRequest(AnalyzeCodeRequest):
    """Request model for code explanation."""
    detail_level: str = Field("medium", description="Detail level: brief, medium, or detailed")


class OptimizeRequest(AnalyzeCodeRequest):
    """Request model for code optimization."""
    focus: Optional[str] = Field(None, description="Focus area: performance, memory, or both")


class SecurityRequest(AnalyzeCodeRequest):
    """Request model for security analysis."""
    include_owasp: bool = Field(True, description="Include OWASP Top 10 categories")


class RefactorRequest(AnalyzeCodeRequest):
    """Request model for code refactoring."""
    target_patterns: Optional[List[str]] = Field(None, description="Design patterns to apply")


class TestRequest(AnalyzeCodeRequest):
    """Request model for test generation."""
    test_framework: str = Field("pytest", description="Test framework: pytest, unittest, jest, etc.")
    test_count: int = Field(5, description="Number of test cases to generate")


class DocumentRequest(AnalyzeCodeRequest):
    """Request model for documentation generation."""
    doc_format: str = Field("google", description="Docstring format: google, numpy, or sphinx")


class ReviewRequest(AnalyzeCodeRequest):
    """Request model for code review."""
    focus_areas: Optional[List[str]] = Field(None, description="Focus areas: security, performance, style, etc.")
