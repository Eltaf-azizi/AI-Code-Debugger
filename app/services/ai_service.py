"""
AI Service - Core AI interaction module
Handles communication with OpenAI API
"""
from typing import Optional, Dict, Any, List
from openai import OpenAI
from datetime import datetime
import hashlib
import json

from app.config import settings
from app.services.prompt_templates import PromptTemplates


class AIService:
    """
    Service for interacting with OpenAI API.
    Handles code analysis, debugging, summarization, and more.
    """
    
    def __init__(self):
        """Initialize AI service with OpenAI client."""
        if not settings.is_configured:
            raise ValueError("OpenAI API Key is not configured")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
    
    def analyze(
        self, 
        code: str, 
        action: str, 
        language: str = "auto",
        additional_context: Optional[str] = None
    ) -> str:
        """
        Analyze code using specified action.
        
        Args:
            code: Source code to analyze
            action: Type of analysis (summarize, debug, explain, optimize, security)
            language: Programming language (auto-detect if not specified)
            additional_context: Optional additional context for the analysis
            
        Returns:
            AI response as string
        """
        # Get system prompt based on action
        system_prompt = self._get_system_prompt(action)
        
        # Build user prompt
        if language == "auto":
            user_prompt = PromptTemplates.get_multi_language_prompt(code)
        else:
            user_prompt = PromptTemplates.get_user_prompt(code, language)
        
        # Add action-specific context
        if additional_context:
            user_prompt += f"\n\n{additional_context}"
        
        user_prompt += self._get_action_context(action)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_structured(
        self,
        code: str,
        action: str,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Analyze code and return structured JSON response.
        
        Args:
            code: Source code to analyze
            action: Type of analysis
            language: Programming language
            
        Returns:
            Parsed JSON response from AI
        """
        # Get system prompt with JSON instruction
        system_prompt = self._get_system_prompt(action)
        system_prompt += "\n\nIMPORTANT: Always respond with valid JSON only. No markdown formatting."
        
        # Build user prompt
        if language == "auto":
            user_prompt = PromptTemplates.get_multi_language_prompt(code)
        else:
            user_prompt = PromptTemplates.get_user_prompt(code, language)
        
        user_prompt += "\n\n" + self._get_json_schema_context(action)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except json.JSONDecodeError as e:
            return {"error": "Failed to parse JSON response", "raw": str(e)}
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_chunked(
        self,
        code: str,
        action: str,
        language: str = "auto",
        chunk_size: int = 4000
    ) -> Dict[str, Any]:
        """
        Analyze large code files by chunking.
        
        Args:
            code: Source code to analyze
            action: Type of analysis
            language: Programming language
            chunk_size: Maximum tokens per chunk
            
        Returns:
            Combined analysis results
        """
        from app.core.chunking import chunk_code
        
        chunks = chunk_code(code, chunk_size)
        results = []
        
        for i, chunk in enumerate(chunks):
            result = self.analyze(chunk, action, language)
            results.append({
                "chunk_index": i,
                "result": result
            })
        
        # Combine results
        combined = self._combine_chunk_results(results, action)
        return combined
    
    def _get_system_prompt(self, action: str) -> str:
        """Get system prompt for specified action."""
        prompts = {
            "summarize": PromptTemplates.SUMMARIZE_SYSTEM,
            "debug": PromptTemplates.DEBUG_SYSTEM,
            "explain": PromptTemplates.EXPLAIN_SYSTEM,
            "optimize": PromptTemplates.OPTIMIZE_SYSTEM,
            "security": PromptTemplates.SECURITY_SYSTEM,
            "refactor": PromptTemplates.REFACTOR_SYSTEM,
            "test": PromptTemplates.TEST_GENERATION_SYSTEM,
            "document": PromptTemplates.DOCUMENTATION_SYSTEM,
            "review": PromptTemplates.CODE_REVIEW_SYSTEM,
        }
        return prompts.get(action, PromptTemplates.EXPLAIN_SYSTEM)
    
    def _get_action_context(self, action: str) -> str:
        """Get additional context for specific action."""
        contexts = {
            "debug": "\n\nFocus on identifying bugs, errors, and potential issues. Provide fixed code.",
            "optimize": "\n\nFocus on performance improvements, algorithmic optimizations, and best practices.",
            "security": "\n\nFocus on security vulnerabilities, OWASP Top 10, and secure coding practices.",
            "test": "\n\nGenerate comprehensive unit tests using pytest for Python or equivalent for other languages.",
            "document": "\n\nGenerate detailed documentation including docstrings, comments, and README.",
            "summarize": "\n\nProvide a concise summary of the code including its purpose, key functions, and complexity.",
        }
        return contexts.get(action, "")
    
    def _get_json_schema_context(self, action: str) -> str:
        """Get JSON schema context for structured output."""
        schemas = {
            "summarize": """
Provide JSON with this exact structure:
{
    "file_summary": "string",
    "functions": [{"name": "string", "summary": "string"}],
    "classes": [{"name": "string", "summary": "string"}],
    "complexity_level": "Low|Medium|High"
}""",
            "debug": """
Provide JSON with this exact structure:
{
    "syntax_errors": [{"line": number, "error": "string", "fix": "string"}],
    "logical_issues": [{"line": number, "issue": "string", "suggestion": "string"}],
    "corrected_code": "string"
}""",
            "security": """
Provide JSON with this exact structure:
{
    "security_risks": [{"line": number, "risk": "string", "severity": "Critical|High|Medium|Low", "fix": "string"}]
}""",
            "optimize": """
Provide JSON with this exact structure:
{
    "performance_suggestions": [{"line": number, "issue": "string", "improvement": "string"}],
    "refactor_suggestions": [{"area": "string", "suggestion": "string"}]
}""",
        }
        return schemas.get(action, "")
    
    def _combine_chunk_results(
        self, 
        results: List[Dict], 
        action: str
    ) -> Dict[str, Any]:
        """Combine results from multiple chunks."""
        if len(results) == 1:
            return {"result": results[0]["result"]}
        
        # For now, return simple combination
        combined_results = [r["result"] for r in results]
        
        # Analyze all chunks together for final result
        combined_prompt = f"Combine these analysis results into a coherent summary:\n\n"
        combined_prompt += "\n\n---\n\n".join(combined_results)
        
        final_result = self.analyze(combined_prompt, action)
        
        return {
            "chunks_processed": len(results),
            "combined_result": final_result
        }
