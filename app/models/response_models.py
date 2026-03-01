"""
Response Models
Pydantic models for API responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ============== Summarize Response ==============

class FunctionSummary(BaseModel):
    """Function summary."""
    name: str
    summary: str


class ClassSummary(BaseModel):
    """Class summary."""
    name: str
    summary: str


class SummarizeResponse(BaseResponse):
    """Response model for code summarization."""
    file_summary: str
    functions: List[FunctionSummary] = []
    classes: List[ClassSummary] = []
    complexity_level: str  # Low, Medium, High


# ============== Debug Response ==============

class SyntaxError(BaseModel):
    """Syntax error."""
    line: int
    error: str
    fix: str


class LogicalIssue(BaseModel):
    """Logical issue."""
    line: int
    issue: str
    suggestion: str


class DebugResponse(BaseResponse):
    """Response model for debugging."""
    syntax_errors: List[SyntaxError] = []
    logical_issues: List[LogicalIssue] = []
    corrected_code: Optional[str] = None


# ============== Explain Response ==============

class ExplainResponse(BaseResponse):
    """Response model for code explanation."""
    overview: str
    line_by_line: Optional[Dict[str, str]] = None
    key_concepts: List[str] = []
    complexity: Optional[str] = None
    dependencies: List[str] = []


# ============== Security Response ==============

class SecurityRisk(BaseModel):
    """Security risk."""
    line: int
    risk: str
    severity: str  # Critical, High, Medium, Low
    fix: str


class SecurityResponse(BaseResponse):
    """Response model for security analysis."""
    security_risks: List[SecurityRisk] = []
    risk_score: float = 0.0  # 0-100


# ============== Optimize Response ==============

class PerformanceSuggestion(BaseModel):
    """Performance suggestion."""
    line: int
    issue: str
    improvement: str


class RefactorSuggestion(BaseModel):
    """Refactoring suggestion."""
    area: str
    suggestion: str


class OptimizeResponse(BaseResponse):
    """Response model for optimization."""
    performance_suggestions: List[PerformanceSuggestion] = []
    refactor_suggestions: List[RefactorSuggestion] = []
    optimized_code: Optional[str] = None


# ============== Health Response ==============

class HealthStatus(BaseModel):
    """Health status."""
    status: str  # healthy, degraded, unhealthy
    checks: Dict[str, Any] = {}


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str
    uptime: float  # seconds
    checks: Dict[str, Any] = {}
