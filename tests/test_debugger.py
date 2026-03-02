"""
Tests for the Debugger Service
"""
import pytest
from unittest.mock import Mock, patch
from app.services.debugger_service import DebuggerService


class TestDebuggerService:
    """Test cases for DebuggerService."""
    
    @pytest.fixture
    def mock_ai_service(self):
        """Create a mock AI service."""
        mock = Mock()
        mock.analyze_structured.return_value = {
            "syntax_errors": [],
            "logical_issues": [{"line": 5, "issue": "Potential None", "suggestion": "Add null check"}],
            "corrected_code": "def fixed():\n    return 42"
        }
        mock.analyze.return_value = "Debug analysis complete"
        return mock
    
    def test_debug_with_language(self, mock_ai_service):
        """Test debugging with specified language."""
        service = DebuggerService(mock_ai_service)
        result = service.debug("code", language="python")
        
        assert "ai_analysis" in result
        mock_ai_service.analyze_structured.assert_called()
    
    def test_debug_auto_detect(self, mock_ai_service):
        """Test debugging with auto language detection."""
        service = DebuggerService(mock_ai_service)
        result = service.debug("def test(): pass", language="auto")
        
        assert result["language"] == "python"
    
    def test_find_bugs(self, mock_ai_service):
        """Test finding bugs in code."""
        service = DebuggerService(mock_ai_service)
        result = service.find_bugs("buggy code", language="python")
        
        mock_ai_service.analyze_structured.assert_called()
    
    def test_suggest_fixes(self, mock_ai_service):
        """Test suggesting fixes."""
        service = DebuggerService(mock_ai_service)
        result = service.suggest_fixes("code", language="python")
        
        assert result is not None
    
    @patch('app.services.debugger_service.error_parser')
    def test_static_analysis_python(self, mock_error_parser, mock_ai_service):
        """Test static analysis for Python."""
        mock_error_parser.parse_python_errors.return_value = []
        
        service = DebuggerService(mock_ai_service)
        result = service._run_static_analysis("valid code", "python")
        
        assert "syntax_errors" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
