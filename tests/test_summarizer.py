"""
Tests for the Summarizer Service
"""
import pytest
from unittest.mock import Mock, patch
from app.services.summarizer_service import SummarizerService


class TestSummarizerService:
    """Test cases for SummarizerService."""
    
    @pytest.fixture
    def mock_ai_service(self):
        """Create a mock AI service."""
        mock = Mock()
        mock.analyze_structured.return_value = {
            "file_summary": "Test summary",
            "functions": [{"name": "test_func", "summary": "Test function"}],
            "classes": [],
            "complexity_level": "Low"
        }
        mock.analyze.return_value = "Simple summary"
        return mock
    
    def test_summarize_with_language(self, mock_ai_service):
        """Test summarization with specified language."""
        service = SummarizerService(mock_ai_service)
        result = service.summarize("print('hello')", language="python")
        
        assert result["file_summary"] == "Test summary"
        mock_ai_service.analyze_structured.assert_called_once()
    
    def test_summarize_auto_detect(self, mock_ai_service):
        """Test summarization with auto language detection."""
        service = SummarizerService(mock_ai_service)
        result = service.summarize("def test(): pass", language="auto")
        
        mock_ai_service.analyze_structured.assert_called_once()
    
    def test_summarize_unstructured(self, mock_ai_service):
        """Test summarization with unstructured response."""
        service = SummarizerService(mock_ai_service)
        result = service.summarize("code", structured=False)
        
        assert "summary" in result
    
    def test_summarize_file_with_filename(self, mock_ai_service):
        """Test file summarization with filename."""
        service = SummarizerService(mock_ai_service)
        result = service.summarize_file("code", filename="test.py")
        
        mock_ai_service.analyze_structured.assert_called_once()
    
    def test_detect_language_from_filename(self, mock_ai_service):
        """Test language detection from filename."""
        service = SummarizerService(mock_ai_service)
        
        assert service._detect_language_from_filename("test.py") == "python"
        assert service._detect_language_from_filename("test.js") == "javascript"
        assert service._detect_language_from_filename("test.ts") == "typescript"
        assert service._detect_language_from_filename("test.java") == "java"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
