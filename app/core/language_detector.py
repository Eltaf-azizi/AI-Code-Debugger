"""
Language Detector Module
Detect programming language from code content
"""
from typing import Dict, Optional, List, Tuple
import re


class LanguageDetector:
    """
    Detect programming language from code content.
    Uses heuristic analysis for accurate detection.
    """
    
    # Language patterns with weights
    PATTERNS = {
        "python": [
            (r'\bdef\s+\w+\s*\(', 3),
            (r'\bimport\s+\w+', 2),
            (r'\bfrom\s+\w+\s+import', 2),
            (r'\bclass\s+\w+.*:', 3),
            (r'\bself\.', 2),
            (r'\bprint\s*\(', 2),
            (r'if\s+__name__\s*==\s*["\']__main__["\']', 3),
            (r':\s*$', 1),  # Colon at end of line (Python specific)
            (r'^\s*#', 1),  # Comments
            (r'\bNone\b', 1),
            (r'\belif\b', 2),
        ],
        "javascript": [
            (r'\bfunction\s+\w+\s*\(', 3),
            (r'\bconst\s+\w+\s*=', 2),
            (r'\blet\s+\w+\s*=', 2),
            (r'\bvar\s+\w+\s*=', 1),
            (r'=>', 2),
            (r'\brequire\s*\(', 2),
            (r'\bexport\s+', 2),
            (r'\bimport\s+.*\s+from', 2),
            (r'\bconsole\.log', 2),
            (r'\btypeof\s+', 1),
            (r'\$\{', 1),  # Template literals
        ],
        "typescript": [
            (r'\binterface\s+\w+', 3),
            (r':\s*(string|number|boolean|any|void|never)\b', 3),
            (r'<\w+>', 2),  # Generics
            (r'\bas\s+\w+', 2),  # Type assertion
            (r':\s*\w+\[\]', 2),  # Array type
            (r'\bexport\s+interface', 3),
            (r'\bexport\s+type', 3),
        ],
        "java": [
            (r'\bpublic\s+class\s+\w+', 3),
            (r'\bprivate\s+\w+', 2),
            (r'\bprotected\s+\w+', 2),
            (r'\bSystem\.out\.println', 3),
            (r'\bimport\s+java\.', 2),
            (r'\bvoid\s+main\s*\(', 3),
            (r'@Override', 2),
            (r'\bnew\s+\w+\s*\(', 1),
        ],
        "c#": [
            (r'\busing\s+System', 2),
            (r'\bnamespace\s+\w+', 2),
            (r'\bpublic\s+class\s+\w+', 2),
            (r'\bConsole\.WriteLine', 3),
            (r'\bstring\[\]', 2),
            (r'\bvar\s+\w+\s*=', 1),
            (r'\basync\s+Task', 2),
        ],
        "c++": [
            (r'#include\s*<', 3),
            (r'\bstd::', 3),
            (r'\bcout\s*<<', 3),
            (r'\bcin\s*>>', 2),
            (r'\bint\s+main\s*\(', 3),
            (r'\bnullptr\b', 2),
            (r'\btemplate\s*<', 2),
        ],
        "go": [
            (r'\bpackage\s+\w+', 3),
            (r'\bfunc\s+\w+\s*\(', 2),
            (r'\bfmt\.', 2),
            (r'\bimport\s+\(', 2),
            (r'\bgo\s+func', 2),
            (r'\b:=\s*', 2),
            (r'\bchan\s+\w+', 2),
        ],
        "rust": [
            (r'\bfn\s+\w+\s*\(', 3),
            (r'\blet\s+mut\s+', 2),
            (r'\bimpl\s+\w+', 2),
            (r'\bpub\s+fn', 2),
            (r'\buse\s+std::', 2),
            (r'->\s*\w+', 2),
            (r'\bmatch\s+\w+', 2),
            (r'\bOption<', 2),
            (r'\bResult<', 2),
        ],
        "ruby": [
            (r'\bdef\s+\w+', 2),
            (r'\bend\b', 2),
            (r'\bputs\s+', 2),
            (r'\brequire\s+', 2),
            (r'\bclass\s+\w+\s*<', 2),
            (r'\battr_accessor\b', 2),
            (r'\bdo\s*\|', 1),
        ],
        "php": [
            (r'<\?php', 3),
            (r'\$\w+', 2),  # Variables
            (r'\bfunction\s+\w+\s*\(', 2),
            (r'\becho\s+', 2),
            (r'\bclass\s+\w+\s*\{', 2),
            (r'->\w+', 1),
        ],
        "swift": [
            (r'\bfunc\s+\w+\s*\(', 2),
            (r'\bvar\s+\w+\s*:', 2),
            (r'\blet\s+\w+\s*:', 2),
            (r'\bclass\s+\w+\s*:', 2),
            (r'\bstruct\s+\w+', 2),
            (r'\bguard\s+let', 2),
            (r'\bif\s+let', 1),
        ],
        "kotlin": [
            (r'\bfun\s+\w+\s*\(', 3),
            (r'\bval\s+\w+\s*:', 2),
            (r'\bvar\s+\w+\s*:', 2),
            (r'\bclass\s+\w+', 2),
            (r'\bdata\s+class', 3),
            (r'\bobject\s+\w+', 2),
            (r'\bcompanion\s+object', 3),
        ],
        "sql": [
            (r'\bSELECT\s+', 3),
            (r'\bFROM\s+', 2),
            (r'\bWHERE\s+', 2),
            (r'\bINSERT\s+INTO', 3),
            (r'\bUPDATE\s+\w+\s+SET', 3),
            (r'\bCREATE\s+TABLE', 3),
            (r'\bJOIN\s+', 2),
        ],
        "html": [
            (r'<!DOCTYPE\s+html>', 3),
            (r'<html', 2),
            (r'<head>', 2),
            (r'<body>', 2),
            (r'<div', 1),
            (r'<span', 1),
            (r'<script', 1),
            (r'<style', 1),
        ],
        "css": [
            (r'\{\s*[\w-]+\s*:', 2),
            (r'@media\s*\(', 2),
            (r'@import\s+', 2),
            (r'\.[\w-]+\s*\{', 2),  # Classes
            (r'#[\w-]+\s*\{', 2),  # IDs
        ],
    }
    
    @classmethod
    def detect(cls, code: str) -> Tuple[str, float]:
        """
        Detect language from code.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Tuple of (language, confidence)
        """
        scores: Dict[str, float] = {}
        
        for language, patterns in cls.PATTERNS.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, code, re.MULTILINE | re.IGNORECASE))
                score += matches * weight
            scores[language] = score
        
        if not scores or max(scores.values()) == 0:
            return "unknown", 0.0
        
        # Normalize confidence
        max_score = max(scores.values())
        detected_language = max(scores, key=scores.get)
        confidence = min(max_score / 10, 1.0)  # Cap at 1.0
        
        return detected_language, confidence
    
    @classmethod
    def detect_with_fallback(cls, code: str) -> str:
        """
        Detect language with fallback to 'text'.
        
        Args:
            code: Source code
            
        Returns:
            Detected language or 'text'
        """
        language, confidence = cls.detect(code)
        
        if confidence < 0.1:
            return "text"
        
        return language


# Convenience function
def detect_language(code: str) -> str:
    """
    Detect programming language from code.
    
    Args:
        code: Source code
        
    Returns:
        Detected language name
    """
    return LanguageDetector.detect_with_fallback(code)
