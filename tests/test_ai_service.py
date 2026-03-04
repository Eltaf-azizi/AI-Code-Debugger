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
    

    def test_analyze_structured(self, mock_settings):
        """Test analyze_structured method."""
        from app.services.ai_service import AIService
        
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"file_summary": "test", "functions": [], "classes": [], "complexity_level": "Low"}'
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch('app.services.ai_service.OpenAI', return_value=mock_client):
            service = AIService()
            result = service.analyze_structured("print('hello')", "summarize", "python")
            
            assert result["file_summary"] == "test"
            assert result["complexity_level"] == "Low"
    
    def test_get_system_prompt(self, mock_settings):
        """Test system prompt retrieval."""
        from app.services.ai_service import AIService
        service = AIService()
        
        summarize_prompt = service._get_system_prompt("summarize")
        debug_prompt = service._get_system_prompt("debug")
        
        assert summarize_prompt is not None
        assert debug_prompt is not None
    
    def test_get_action_context(self, mock_settings):
        """Test action context retrieval."""
        from app.services.ai_service import AIService
        service = AIService()
        
        debug_context = service._get_action_context("debug")
        optimize_context = service._get_action_context("optimize")
        
        assert "bugs" in debug_context.lower() or "bug" in debug_context.lower()
        assert "performance" in optimize_context.lower()


class TestPromptTemplates:
    """Test prompt templates."""
    
    def test_all_prompts_exist(self):
        """Test all prompt templates exist."""
        from app.services.prompt_templates import PromptTemplates
        
        assert PromptTemplates.EXPLAIN_SYSTEM is not None
        assert PromptTemplates.DEBUG_SYSTEM is not None
        assert PromptTemplates.OPTIMIZE_SYSTEM is not None
        assert PromptTemplates.SECURITY_SYSTEM is not None
        assert PromptTemplates.SUMMARIZE_SYSTEM is not None
    
    def test_get_user_prompt(self):
        """Test user prompt generation."""
        from app.services.prompt_templates import PromptTemplates
        
        code = "def hello():\n    print('hello')"
        prompt = PromptTemplates.get_user_prompt(code, "python")
        
        assert code in prompt
    
    def test_get_multi_language_prompt(self):
        """Test multi-language prompt generation."""
        from app.services.prompt_templates import PromptTemplates
        
        code = "def hello():\n    print('hello')"
        prompt = PromptTemplates.get_multi_language_prompt(code)
        
        assert code in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
