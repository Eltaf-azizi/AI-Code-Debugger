"""
Tokenization Module
Count and limit tokens for AI processing
"""
import re
from typing import List, Tuple


def count_tokens(text: str) -> int:
    """
    Estimate token count for text.
    Uses a simple approximation: ~4 characters per token.
    
    Args:
        text: Text to count tokens for
        
    Returns:
        Estimated token count
    """
    # More accurate estimation using word counting
    # Split by whitespace
    words = re.findall(r'\b\w+\b', text)
    
    # Average token is about 0.75 words for code
    # Plus special characters add tokens
    special_chars = len(re.findall(r'[^\w\s]', text))
    
    tokens = len(words) * 1.3 + special_chars * 0.5
    
    return int(tokens)


def truncate_to_token_limit(
    text: str, 
    max_tokens: int,
    preserve_end: bool = True
) -> str:
    """
    Truncate text to fit within token limit.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum tokens allowed
        preserve_end: Whether to preserve end of text
        
    Returns:
        Truncated text
    """
    char_limit = max_tokens * 4  # Approximate
    
    if len(text) <= char_limit:
        return text
    
    if preserve_end:
        # Keep beginning and end
        half_limit = char_limit // 2
        return text[:half_limit] + "\n\n... [truncated] ...\n\n" + text[-half_limit:]
    else:
        return text[:char_limit] + "\n\n... [truncated]"


def split_into_tokens(text: str, chunk_size: int) -> List[str]:
    """
    Split text into token-sized chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum tokens per chunk
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for word in words:
        word_tokens = count_tokens(word)
        
        if current_tokens + word_tokens > chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_tokens = word_tokens
        else:
            current_chunk.append(word)
            current_tokens += word_tokens
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def estimate_completion_tokens(
    prompt_tokens: int, 
    max_response_tokens: int,
    model_max: int = 4096
) -> int:
    """
    Estimate safe completion tokens based on prompt.
    
    Args:
        prompt_tokens: Number of tokens in prompt
        max_response_tokens: Desired max response tokens
        model_max: Maximum tokens for the model
        
    Returns:
        Safe number of tokens for completion
    """
    available = model_max - prompt_tokens
    return min(max_response_tokens, available)
