"""
Tests for AI Service
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture(autouse=True)
def mock_settings():
    """Mock settings for all tests."""
    with patch('app.services.ai_service.settings') as mock:
        mock.OPENAI_API_KEY = "test-key"
        mock.MODEL_NAME = "gpt-4"
        mock.TEMPERATURE = 0.5
        mock.MAX_TOKENS = 4000
        mock.is_configured = True
        yield mock


@pytest.fixture
def mock_openai():
    """Mock OpenAI client."""
    with patch('app.services.ai_service.OpenAI') as mock:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock.return_value = mock_client
        yield mock_client


class TestAIService:
    """Test AI service."""
    
    def test_service_init(self, mock_settings):
        """Test AI service initialization."""
        from app.services.ai_service import AIService
        service = AIService()
        assert service is not None
        assert service.model == "gpt-4"
        assert service.temperature == 0.5
    
    def test_service_init_without_key(self, mock_settings):
        """Test AI service fails without API key."""
        from app.services.ai_service import AIService
        mock_settings.is_configured = False
        mock_settings.OPENAI_API_KEY = None
        
        with pytest.raises(ValueError):
            AIService()
    
    def test_analyze_returns_response(self, mock_settings, mock_openai):
        """Test analyze method returns response."""
        from app.services.ai_service import AIService
        service = AIService()
        
        result = service.analyze("print('hello')", "explain", "python")
        assert result == "Test response"
    
