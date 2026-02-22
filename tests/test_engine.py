import pytest
from src.core.prompts import PromptTemplates

def test_prompt_templates_exist():
    """Check if prompt templates are loaded correctly."""
    assert PromptTemplates.EXPLAIN_SYSTEM is not None
    assert PromptTemplates.DEBUG_SYSTEM is not None
    assert PromptTemplates.OPTIMIZE_SYSTEM is not None

def test_user_prompt_generation():
    """Check if user prompt formats the code correctly."""
    code = "print('hello')"
    prompt = PromptTemplates.get_user_prompt(code)
    assert code in prompt
    assert "Analyze the following code snippet:" in prompt

# Note: Testing the AI Engine requires mocking the OpenAI API client
# which is an advanced topic, but here is a basic structure check.
def test_engine_init_fails_without_key(monkeypatch):
    """Test that engine raises error if no key is found."""
    from src.utils.config import settings
    from src.core.ai_engine import CodeAnalyzer
    
    # Temporarily remove the key
    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    
    with pytest.raises(ValueError):
        CodeAnalyzer()
