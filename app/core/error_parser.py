"""
Error Parser Module
Parse syntax errors from various programming languages
"""
import ast
import re
from typing import List, Dict, Any, Optional, Tuple


def parse_python_errors(code: str) -> List[Dict[str, Any]]:
    """
    Parse Python syntax errors.
    
    Args:
        code: Python source code
        
    Returns:
        List of error dictionaries with line, error, and fix
    """
    errors = []
    
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append({
            "line": e.lineno,
            "column": e.offset,
            "error": e.msg,
            "fix": _suggest_python_fix(e),
            "severity": "critical"
        })
    except Exception as e:
        errors.append({
            "line": 1,
            "error": str(e),
            "fix": "Please check the code manually",
            "severity": "error"
        })
    
    return errors


def _suggest_python_fix(error: SyntaxError) -> str:
    """Suggest fix for Python syntax error."""
    msg = error.msg.lower()
    
    if "invalid syntax" in msg:
        # Common issues
        if error.text and ':' not in error.text.rstrip():
            return "Add ':' at the end of the statement"
        return "Check for missing brackets, parentheses, or quotes"
    
    if "unexpected token" in msg or "invalid token" in msg:
        return "Remove or replace the unexpected character"
    
    if "EOL" in msg or "end of line" in msg:
        return "Complete the string or check for missing closing quotes"
    
    if "EOF" in msg or "end of file" in msg:
        return "Add closing bracket or statement"
    
    if "unindent" in msg:
        return "Fix indentation to match previous lines"
    
    return "Review the syntax at this line"


def parse_javascript_errors(code: str) -> List[Dict[str, Any]]:
    """
    Parse JavaScript syntax errors.
    
    Args:
        code: JavaScript source code
        
    Returns:
        List of error dictionaries
    """
    errors = []
    
    # Use basic pattern matching for common JS errors
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Check for common issues
        if _check_js_unbalanced_brackets(line):
            errors.append({
                "line": i,
                "error": "Unbalanced brackets",
                "fix": "Ensure all brackets are properly closed",
                "severity": "critical"
            })
        
        if _check_js_unbalanced_parens(line):
            errors.append({
                "line": i,
                "error": "Unbalanced parentheses",
                "fix": "Ensure all parentheses are properly closed",
                "severity": "critical"
            })
    
    return errors


def _check_js_unbalanced_brackets(line: str) -> bool:
    """Check for unbalanced brackets."""
    opens = line.count('{')
    closes = line.count('}')
    return opens > 0 and opens != closes


def _check_js_unbalanced_parens(line: str) -> bool:
    """Check for unbalanced parentheses."""
    opens = line.count('(')
    closes = line.count(')')
    return opens > 0 and opens != closes


def extract_error_info(error_message: str) -> Dict[str, Any]:
    """
    Extract structured info from error message.
    
    Args:
        error_message: Raw error message
        
    Returns:
        Structured error information
    """
    info = {
        "message": error_message,
        "line": None,
        "column": None,
        "type": "unknown"
    }
    
    # Try to extract line number
    line_match = re.search(r'line\s+(\d+)', error_message, re.IGNORECASE)
    if line_match:
        info["line"] = int(line_match.group(1))
    
    # Try to extract column
    col_match = re.search(r'column\s+(\d+)', error_message, re.IGNORECASE)
    if col_match:
        info["column"] = int(col_match.group(1))
    
    # Determine error type
    if "syntax" in error_message.lower():
        info["type"] = "syntax"
    elif "reference" in error_message.lower():
        info["type"] = "reference"
    elif "type" in error_message.lower():
        info["type"] = "type"
    elif "name" in error_message.lower():
        info["type"] = "name"
    
    return info


def format_error_for_display(error: Dict[str, Any]) -> str:
    """
    Format error for human-readable display.
    
    Args:
        error: Error dictionary
        
    Returns:
        Formatted error string
    """
    line = error.get("line", "?")
    msg = error.get("error", "Unknown error")
    fix = error.get("fix", "")
    
    result = f"Line {line}: {msg}"
    if fix:
        result += f"\n  → {fix}"
    
    return result
