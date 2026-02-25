"""
Unit tests for the AI Code Debugger engine.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.prompts detect_language
from import PromptTemplates, src.core.ai_engine import CodeAnalyzer, DebuggingSession, AnalysisResult


class TestPromptTemplates:
    """Tests for prompt templates."""
    
    def test_prompt_templates_exist(self):
        """Check if all prompt templates are loaded."""
        assert PromptTemplates.EXPLAIN_SYSTEM is not None
        assert PromptTemplates.DEBUG_SYSTEM is not None
        assert PromptTemplates.OPTIMIZE_SYSTEM is not None
        assert PromptTemplates.SECURITY_SYSTEM is not None
        assert PromptTemplates.REFACTOR_SYSTEM is not None
        assert PromptTemplates.TEST_GENERATION_SYSTEM is not None
        assert PromptTemplates.DOCUMENTATION_SYSTEM is not None
        assert PromptTemplates.CODE_REVIEW_SYSTEM is not None
    
    def test_user_prompt_generation(self):
        """Check if user prompt formats code correctly."""
        code = "print('hello')"
        prompt = PromptTemplates.get_user_prompt(code)
        assert code in prompt
        assert "Analyze the following" in prompt
    
    def test_multi_language_prompt(self):
        """Check multi-language prompt generation."""
        code = "def foo(): pass"
        prompt = PromptTemplates.get_multi_language_prompt(code)
        assert code in prompt
        assert "identify the programming language" in prompt
    
    def test_debug_with_context_prompt(self):
        """Check debug prompt with context."""
        code = "def foo(): pass"
        error = "NameError: name 'x' is not defined"
        prompt = PromptTemplates.get_debug_with_context_prompt(code, error)
        assert code in prompt
        assert error in prompt
    
    def test_project_analysis_prompt(self):
        """Check project analysis prompt."""
        files = {"main.py": "print('hello')", "utils.py": "def foo(): pass"}
        prompt = PromptTemplates.get_project_analysis_prompt(files)
        assert "main.py" in prompt
        assert "utils.py" in prompt


class TestLanguageDetection:
    """Tests for language detection."""
    
    def test_detect_python(self):
        """Test Python detection."""
        code = "def foo():\n    print('hello')"
        assert detect_language(code) == "python"
    
    def test_detect_javascript(self):
        """Test JavaScript detection."""
        code = "function foo() { console.log('hello'); }"
        assert detect_language(code) == "javascript"
    
    def test_detect_java(self):
        """Test Java detection."""
        code = "public class Main { public static void main(String[] args) {} }"
        assert detect_language(code) == "java"
    
    def test_detect_rust(self):
        """Test Rust detection."""
        code = "fn main() { println!(\"Hello\"); }"
        assert detect_language(code) == "rust"
    
    def test_detect_unknown(self):
        """Test unknown language."""
        code = "random text without specific patterns"
        assert detect_language(code) == "text"


class TestDebuggingSession:
    """Tests for debugging session."""
    
    def test_session_creation(self):
        """Test session initialization."""
        session = DebuggingSession("code", "python", "Debug")
        assert session.code == "code"
        assert session.language == "python"
        assert session.action == "Debug"
        assert session.id is not None
    
    def test_session_to_dict(self):
        """Test session serialization."""
        session = DebuggingSession("code", "python", "Debug")
        session.result = "Fixed!"
        data = session.to_dict()
        
        assert data["code"] == "code"
        assert data["language"] == "python"
        assert data["action"] == "Debug"
        assert data["result"] == "Fixed!"


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer class."""
    
    @patch('src.core.ai_engine.OpenAI')
    def test_analyzer_init(self, mock_openai):
        """Test analyzer initialization with API key."""
        with patch('src.core.ai_engine.settings') as mock_settings:
            mock_settings.is_configured = True
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.MODEL_NAME = "gpt-4"
            mock_settings.MAX_TOKENS = 4000
            
            analyzer = CodeAnalyzer()
            assert analyzer is not None
    
    def test_analyzer_init_without_key(self):
        """Test analyzer initialization fails without API key."""
        with patch('src.core.ai_engine.settings') as mock_settings:
            mock_settings.is_configured = False
            
            with pytest.raises(ValueError):
                CodeAnalyzer()
    
    def test_action_prompts_mapping(self):
        """Test action prompts are correctly mapped."""
        assert "Explain" in CodeAnalyzer.ACTION_PROMPTS
        assert "Debug" in CodeAnalyzer.ACTION_PROMPTS
        assert "Optimize" in CodeAnalyzer.ACTION_PROMPTS
        assert "Security" in CodeAnalyzer.ACTION_PROMPTS
        assert "Refactor" in CodeAnalyzer.ACTION_PROMPTS
        assert "Generate Tests" in CodeAnalyzer.ACTION_PROMPTS
        assert "Document" in CodeAnalyzer.ACTION_PROMPTS
        assert "Review" in CodeAnalyzer.ACTION_PROMPTS


class TestAnalysisResult:
    """Tests for AnalysisResult class."""
    
    def test_parse_response_with_code(self):
        """Test response parsing with code blocks."""
        response = """Here is the fixed code:

```python
def foo():
    return 42
```

This fixes the issue."""
        
        result = AnalysisResult(response, "Debug")
        assert result.fixed_code is not None
        assert "def foo" in result.fixed_code
    
    def test_parse_empty_response(self):
        """Test parsing empty response."""
        result = AnalysisResult("", "Debug")
        assert result.raw_response == ""
        assert result.action == "Debug"


# Integration-style tests (mocked)
class TestAnalyzerIntegration:
    """Integration tests with mocked API."""
    
    @patch('src.core.ai_engine.OpenAI')
    def test_analyze_returns_result(self, mock_openai):
        """Test analyze method returns result."""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Analysis result"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        with patch('src.core.ai_engine.settings') as mock_settings:
            mock_settings.is_configured = True
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.MODEL_NAME = "gpt-4"
            mock_settings.MAX_TOKENS = 4000
            
            analyzer = CodeAnalyzer()
            result = analyzer.analyze("code", "Explain")
            
            assert result == "Analysis result"
    
    @patch('src.core.ai_engine.OpenAI')
    def test_session_tracking(self, mock_openai):
        """Test that sessions are tracked."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Debug result"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        with patch('src.core.ai_engine.settings') as mock_settings:
            mock_settings.is_configured = True
            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.MODEL_NAME = "gpt-4"
            mock_settings.MAX_TOKENS = 4000
            
            analyzer = CodeAnalyzer()
            
            # Clear any existing sessions
            analyzer.clear_history()
            
            # Run analysis
            analyzer.analyze("def buggy(): return 1/0", "Debug")
            
            # Check session was added
            assert len(analyzer.sessions) == 1
            assert analyzer.sessions[0].action == "Debug"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
