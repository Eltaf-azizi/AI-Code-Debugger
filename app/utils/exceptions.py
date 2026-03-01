"""
Custom Exceptions
"""


class AICodeAssistantException(Exception):
    """Base exception for AI Code Assistant."""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ConfigurationError(AICodeAssistantException):
    """Configuration error."""
    pass


class AIServiceError(AICodeAssistantException):
    """AI service error."""
    pass


class AnalysisError(AICodeAssistantException):
    """Analysis error."""
    pass


class ValidationError(AICodeAssistantException):
    """Validation error."""
    pass


class DatabaseError(AICodeAssistantException):
    """Database error."""
    pass


class RateLimitError(AICodeAssistantException):
    """Rate limit exceeded."""
    pass


class AuthenticationError(AICodeAssistantException):
    """Authentication error."""
    pass
