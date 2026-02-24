"""
Enhanced AI Engine for the Advanced AI Code Debugger.
Supports multiple AI actions including debugging, security analysis, refactoring, and more.
"""
from openai import OpenAI
from typing import Dict, List, Optional, Any
import json
import hashlib
from datetime import datetime
from src.utils.config import settings
from src.core.prompts import PromptTemplates


class DebuggingSession:
    """Represents a single debugging session."""
    
    def __init__(self, code: str, language: str, action: str):
        self.id = hashlib.md5(f"{code}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        self.code = code
        self.language = language
        self.action = action
        self.timestamp = datetime.now()
        self.result: Optional[str] = None
        self.errors: List[Dict[str, Any]] = []
        self.fixed_code: Optional[str] = None
        
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "code": self.code,
            "language": self.language,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "result": self.result,
            "errors": self.errors,
            "fixed_code": self.fixed_code
        }


class AnalysisResult:
    """Structured result from code analysis."""
    
    def __init__(self, raw_response: str, action: str):
        self.raw_response = raw_response
        self.action = action
        self.issues: List[Dict[str, Any]] = []
        self.fixed_code: Optional[str] = None
        self.explanation: Optional[str] = None
        self.suggestions: List[str] = []
        self.parse_response()
        
    def parse_response(self):
        """Parse the raw AI response into structured data."""
        # Extract code blocks if present
        if "```" in self.raw_response:
            parts = self.raw_response.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Code block content
                    lang_and_code = part.split("\n", 1)
                    if len(lang_and_code) > 1:
                        self.fixed_code = lang_and_code[1].strip()
                        
        # Extract issues based on action
        if self.action == "Debug":
            self._parse_debug_issues()
        elif self.action == "Security":
            self._parse_security_issues()
            
    def _parse_debug_issues(self):
        """Parse debugging issues from response."""
        lines = self.raw_response.split("\n")
        current_issue = {}
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ["error", "bug", "issue", "problem"]):
                if current_issue:
                    self.issues.append(current_issue)
                current_issue = {"description": line}
            elif "line" in line.lower() or ":" in line:
                if current_issue:
                    current_issue["location"] = line
                    
        if current_issue:
            self.issues.append(current_issue)
            
    def _parse_security_issues(self):
        """Parse security vulnerabilities from response."""
        lines = self.raw_response.split("\n")
        current_vuln = {}
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ["vulnerability", "cve", "risk", "threat"]):
                if current_vuln:
                    self.issues.append(current_vuln)
                current_vuln = {"description": line, "severity": "Unknown"}
                
        if current_vuln:
            self.issues.append(current_vuln)


class CodeAnalyzer:
    """
    Enhanced AI Code Analyzer with support for multiple analysis types.
    """
    
    # Action to system prompt mapping
    ACTION_PROMPTS = {
        "Explain": PromptTemplates.EXPLAIN_SYSTEM,
        "Debug": PromptTemplates.DEBUG_SYSTEM,
        "Optimize": PromptTemplates.OPTIMIZE_SYSTEM,
        "Security": PromptTemplates.SECURITY_SYSTEM,
        "Refactor": PromptTemplates.REFACTOR_SYSTEM,
        "Generate Tests": PromptTemplates.TEST_GENERATION_SYSTEM,
        "Document": PromptTemplates.DOCUMENTATION_SYSTEM,
        "Review": PromptTemplates.CODE_REVIEW_SYSTEM,
    }
    
    def __init__(self):
        if not settings.is_configured:
            raise ValueError("OpenAI API Key is missing. Please check your .env file.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.sessions: List[DebuggingSession] = []
        
    def analyze(self, code: str, action: str, language: str = "auto") -> str:
        """
        Analyze code using the specified action.
        
        Args:
            code: The source code to analyze
            action: The type of analysis (Explain, Debug, Optimize, Security, etc.)
            language: Programming language (auto-detect if not specified)
            
        Returns:
            AI response as string
        """
        # Get the appropriate system prompt
        system_msg = self.ACTION_PROMPTS.get(action, PromptTemplates.EXPLAIN_SYSTEM)
        
        # Get user prompt with language info
        if language == "auto":
            user_prompt = PromptTemplates.get_multi_language_prompt(code)
        else:
            user_prompt = PromptTemplates.get_user_prompt(code, language)
            
        # Add action-specific context
        if action == "Debug":
            user_prompt += "\n\nFocus on identifying bugs, errors, and potential issues. Provide fixed code."
        elif action == "Optimize":
            user_prompt += "\n\nFocus on performance improvements, algorithmic optimizations, and best practices."
        elif action == "Security":
            user_prompt += "\n\nFocus on security vulnerabilities, OWASP Top 10, and secure coding practices."
        elif action == "Generate Tests":
            user_prompt += "\n\nGenerate comprehensive unit tests using pytest for Python or equivalent for other languages."
        elif action == "Document":
            user_prompt += "\n\nGenerate detailed documentation including docstrings, comments, and README."
            
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=settings.MAX_TOKENS,
            )
            
            result = response.choices[0].message.content
            
            # Create and store session
            session = DebuggingSession(code, language, action)
            session.result = result
            self.sessions.append(session)
            
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"
            
    def analyze_with_context(self, code: str, action: str, context: Dict) -> str:
        """
        Analyze code with additional context (error messages, stack traces, etc.)
        
        Args:
            code: The source code
            action: Type of analysis
            context: Additional context (error logs, test failures, etc.)
        """
        system_msg = self.ACTION_PROMPTS.get(action, PromptTemplates.EXPLAIN_SYSTEM)
        
        # Build enhanced prompt with context
        user_prompt = f"""Analyze the following code:

```{context.get('language', 'python')}
{code}
```

Additional Context:
{json.dumps(context, indent=2)}

Please provide a thorough analysis considering the context above."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=settings.MAX_TOKENS,
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
            
    def compare_code(self, original: str, modified: str) -> str:
        """
        Compare two versions of code and explain differences.
        """
        system_msg = """You are a code comparison expert. Your task is to analyze two versions 
        of code and explain the differences in detail. Use a structured format with:
        1. Summary of changes
        2. Line-by-line differences
        3. Impact analysis
        4. Potential benefits and risks"""
        
        user_prompt = f"""Compare these two code versions:

ORIGINAL:
```{original}
```

MODIFIED:
```{modified}
```

Provide a detailed comparison."""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
            
    def get_session_history(self) -> List[Dict]:
        """Get history of all debugging sessions."""
        return [session.to_dict() for session in self.sessions]
        
    def get_session(self, session_id: str) -> Optional[DebuggingSession]:
        """Get a specific session by ID."""
        for session in self.sessions:
            if session.id == session_id:
                return session
        return None
        
    def clear_history(self):
        """Clear all session history."""
        self.sessions.clear()


# Singleton instance
_analyzer: Optional[CodeAnalyzer] = None


def get_analyzer() -> CodeAnalyzer:
    """Get or create the singleton analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = CodeAnalyzer()
    return _analyzer


def reset_analyzer():
    """Reset the analyzer instance (useful for testing or key changes)."""
    global _analyzer
    _analyzer = None
