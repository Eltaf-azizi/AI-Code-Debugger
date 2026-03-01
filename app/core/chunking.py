"""
Code Chunking Module
Split large code files into manageable chunks
"""
from typing import List, Optional


def chunk_code(code: str, chunk_size: int = 4000) -> List[str]:
    """
    Split code into chunks of specified size.
    
    Args:
        code: Source code to chunk
        chunk_size: Maximum tokens per chunk
        
    Returns:
        List of code chunks
    """
    # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
    char_limit = chunk_size * 4
    
    # Split by newlines to preserve code structure
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in lines:
        line_size = len(line)
        
        # If single line is too big, split it
        if line_size > char_limit:
            # Save current chunk if not empty
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split the long line
            for i in range(0, line_size, char_limit):
                chunks.append(line[i:i + char_limit])
            continue
        
        # Check if adding this line would exceed limit
        if current_size + line_size > char_limit:
            # Save current chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = line_size
        else:
            current_chunk.append(line)
            current_size += line_size
    
    # Add remaining chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks if chunks else [code]


def chunk_by_function(code: str, language: str = "python") -> List[str]:
    """
    Split code by functions/classes (smarter chunking).
    
    Args:
        code: Source code
        language: Programming language
        
    Returns:
        List of code chunks by function/class
    """
    if language == "python":
        return _chunk_python_by_function(code)
    elif language in ("javascript", "typescript"):
        return _chunk_js_by_function(code)
    else:
        # Fallback to simple chunking
        return chunk_code(code)


def _chunk_python_by_function(code: str) -> List[str]:
    """Split Python code by functions and classes."""
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Check for function or class definition
        if stripped.startswith('def ') or stripped.startswith('class '):
            # Start new chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
        else:
            current_chunk.append(line)
    
    # Add remaining chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks if chunks else [code]


def _chunk_js_by_function(code: str) -> List[str]:
    """Split JavaScript/TypeScript code by functions."""
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check for function definitions
        if (stripped.startswith('function ') or 
            stripped.startswith('const ') or 
            stripped.startswith('let ') or 
            stripped.startswith('var ') or
            '=>' in stripped):
            # Start new chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
        else:
            current_chunk.append(line)
    
    # Add remaining chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks if chunks else [code]
