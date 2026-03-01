"""
Helper Functions
"""
import hashlib
from typing import Any, Dict
from datetime import datetime


def hash_code(code: str) -> str:
    """
    Generate hash for code.
    
    Args:
        code: Source code
    
    Returns:
        SHA256 hash
    """
    return hashlib.sha256(code.encode()).hexdigest()


def format_timestamp(dt: datetime = None) -> str:
    """
    Format timestamp for API responses.
    
    Args:
        dt: Datetime object (now if not specified)
    
    Returns:
        ISO formatted timestamp
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()


def sanitize_code(code: str, max_length: int = 100000) -> str:
    """
    Sanitize code input.
    
    Args:
        code: Source code
        max_length: Maximum allowed length
    
    Returns:
        Sanitized code
    """
    # Strip whitespace
    code = code.strip()
    
    # Check length
    if len(code) > max_length:
        code = code[:max_length]
    
    return code


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
    
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def truncate_string(s: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to max length.
    
    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to add
    
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix
