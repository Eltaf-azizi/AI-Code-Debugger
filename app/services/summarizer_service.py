"""
Summarizer Service
Code summarization using AI
"""
from typing import Dict, Any, List, Optional

from app.services.ai_service import AIService
from app.services.prompt_templates import detect_language


class SummarizerService:
    """
    Service for code summarization.
    Provides concise summaries of code files and their components.
    """
    
    def __init__(self, ai_service: AIService):
        """Initialize with AI service."""
        self.ai_service = ai_service
    
    def summarize(
        self, 
        code: str, 
        language: Optional[str] = None,
        structured: bool = True
    ) -> Dict[str, Any]:
        """
        Summarize the given code.
        
        Args:
            code: Source code to summarize
            language: Programming language (auto-detected if not specified)
            structured: Whether to return structured JSON
            
        Returns:
            Summarization result
        """
        if language is None or language == "auto":
            language = detect_language(code)
        
        if structured:
            return self.ai_service.analyze_structured(code, "summarize", language)
        else:
            result = self.ai_service.analyze(code, "summarize", language)
            return {"summary": result}
    
    def summarize_file(
        self,
        code: str,
        filename: Optional[str] = None,
        structured: bool = True
    ) -> Dict[str, Any]:
        """
        Summarize a code file.
        
        Args:
            code: Source code
            filename: Optional filename for language hint
            structured: Whether to return structured JSON
            
        Returns:
            File summarization result
        """
        # Try to detect language from filename
        language = None
        if filename:
            language = self._detect_language_from_filename(filename)
        
        return self.summarize(code, language, structured)
    
    def _detect_language_from_filename(self, filename: str) -> Optional[str]:
        """Detect language from file extension."""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'c++',
            '.h': 'c',
            '.hpp': 'c++',
            '.cs': 'c#',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
        }
        
        ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''
        return extensions.get(f'.{ext}')
