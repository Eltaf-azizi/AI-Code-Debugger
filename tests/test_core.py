"""
Tests for Core Utilities
"""
import pytest
from unittest.mock import Mock, patch


class TestChunking:
    """Test code chunking functionality."""
    
    def test_chunk_code_basic(self):
        """Test basic code chunking."""
        from app.core.chunking import chunk_code
        
        code = "line1\nline2\nline3\nline4\nline5"
        chunks = chunk_code(code, chunk_size=2)
        
        assert len(chunks) >= 1
        assert "line1" in chunks[0]
    
    def test_chunk_code_large(self):
        """Test chunking large code."""
        from app.core.chunking import chunk_code
        
        # Create large code
        code = "\n".join([f"line {i}" for i in range(100)])
        chunks = chunk_code(code, chunk_size=20)
        
        assert len(chunks) > 1
    
    def test_chunk_code_empty(self):
        """Test chunking empty code."""
        from app.core.chunking import chunk_code
        
        chunks = chunk_code("", chunk_size=10)
        assert len(chunks) == 0 or (len(chunks) == 1 and chunks[0] == "")


class TestTokenizer:
    """Test tokenizer functionality."""
    
    def test_count_tokens(self):
        """Test token counting."""
        from app.core.tokenizer import count_tokens
        
        code = "def hello():\n    print('hello')"
        tokens = count_tokens(code)
        
        assert tokens > 0
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        from app.core.tokenizer import estimate_tokens
        
        code = "def hello():\n    return 'world'"
        tokens = estimate_tokens(code)
        
        assert tokens > 0
        # Rough estimate: ~4 chars per token
        assert tokens <= len(code) / 2


class TestLanguageDetector:
    """Test language detection."""
    
    def test_detect_python(self):
        """Test Python detection."""
        from app.core.language_detector import detect_language
        
        code = "def hello():\n    print('hello')"
        lang = detect_language(code)
        
        assert lang == "python"
    
    def test_detect_javascript(self):
        """Test JavaScript detection."""
        from app.core.language_detector import detect_language
        
        code = "function hello() { console.log('hello'); }"
        lang = detect_language(code)
        
        assert lang == "javascript"
    
    def test_detect_typescript(self):
        """Test TypeScript detection."""
        from app.core.language_detector import detect_language
        
        code = "function hello(): string { return 'hello'; }"
        lang = detect_language(code)
        
        assert lang == "typescript"
    
    def test_detect_java(self):
        """Test Java detection."""
        from app.core.language_detector import detect_language
        
        code = "public class Main { public static void main(String[] args) {} }"
        lang = detect_language(code)
        
        assert lang == "java"
    
    def test_detect_rust(self):
        """Test Rust detection."""
        from app.core.language_detector import detect_language
        
        code = "fn main() { println!(\"Hello\"); }"
        lang = detect_language(code)
        
        assert lang == "rust"
    
    def test_detect_go(self):
        """Test Go detection."""
        from app.core.language_detector import detect_language
        
        code = "package main\n\nfunc main() { fmt.Println(\"Hello\") }"
        lang = detect_language(code)
        
        assert lang == "go"
    
    def test_detect_cpp(self):
        """Test C++ detection."""
        from app.core.language_detector import detect_language
        
        code = "#include <iostream>\nint main() { std::cout << \"Hello\"; return 0; }"
        lang = detect_language(code)
        
        assert lang in ["cpp", "c++", "c"]
    
    def test_detect_unknown(self):
        """Test unknown language."""
        from app.core.language_detector import detect_language
        
        code = "random text without programming patterns"
        lang = detect_language(code)
        
        assert lang == "text" or lang == "unknown"


class TestErrorParser:
    """Test error parser."""
    
    def test_parse_python_error(self):
        """Test Python error parsing."""
        from app.core.error_parser import parse_error
        
        error_msg = "File \"test.py\", line 10\n    return x\nNameError: name 'x' is not defined"
        parsed = parse_error(error_msg, "python")
        
        assert parsed is not None
        assert "line" in parsed or "error" in str(parsed).lower()
    
    def test_parse_javascript_error(self):
        """Test JavaScript error parsing."""
        from app.core.error_parser import parse_error
        
        error_msg = "ReferenceError: x is not defined\n    at Object.<anonymous> (test.js:5:10)"
        parsed = parse_error(error_msg, "javascript")
        
        assert parsed is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
