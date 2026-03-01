"""
AST Parser
Generic Abstract Syntax Tree parser for multiple languages
"""
import ast
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class ASTNode:
    """Generic AST node representation."""
    type: str
    name: Optional[str] = None
    line: Optional[int] = None
    children: List['ASTNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class ASTParser:
    """
    Generic AST parser.
    Provides unified interface for parsing different languages.
    """
    
    def __init__(self):
        """Initialize AST parser."""
        self.tree: Optional[Any] = None
        self.language: str = "python"
    
    def parse(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Parse code into AST.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Parsed AST as dictionary
        """
        self.language = language
        
        if language == "python":
            return self._parse_python(code)
        elif language in ("javascript", "typescript"):
            return self._parse_js(code)
        else:
            return {"error": f"Unsupported language: {language}"}
    
    def _parse_python(self, code: str) -> Dict[str, Any]:
        """Parse Python code."""
        try:
            tree = ast.parse(code)
            return self._python_ast_to_dict(tree)
        except SyntaxError as e:
            return {"error": str(e)}
    
    def _python_ast_to_dict(self, node: ast.AST) -> Dict[str, Any]:
        """Convert Python AST to dictionary."""
        result = {
            "type": type(node).__name__,
            "line": getattr(node, 'lineno', None)
        }
        
        # Add specific attributes
        if isinstance(node, ast.Name):
            result["name"] = node.id
        elif isinstance(node, ast.Constant):
            result["value"] = repr(node.value)
        elif isinstance(node, ast.FunctionDef):
            result["name"] = node.name
            result["args"] = [arg.arg for arg in node.args.args]
        elif isinstance(node, ast.ClassDef):
            result["name"] = node.name
        
        # Process children
        for child in ast.iter_child_nodes(node):
            child_key = type(child).__name__.lower()
            if child_key not in result:
                result[child_key] = []
            result[child_key].append(self._python_ast_to_dict(child))
        
        return result
    
    def _parse_js(self, code: str) -> Dict[str, Any]:
        """
        Parse JavaScript code (simplified).
        Note: For full JS support, consider using a proper parser like esprima.
        """
        # Simplified JS parsing using regex
        import re
        
        functions = re.findall(
            r'(?:function|const|let|var)\s+(\w+)\s*(?:=\s*)?(?:\([^)]*\))?\s*=>?',
            code
        )
        
        classes = re.findall(r'class\s+(\w+)', code)
        
        return {
            "language": "javascript",
            "functions": functions,
            "classes": classes,
            "note": "Simplified parsing. Use proper JS parser for full AST."
        }
    
    def get_node_at_line(self, code: str, line: int) -> Optional[Dict[str, Any]]:
        """
        Get AST node at specific line.
        
        Args:
            code: Source code
            line: Line number
            
        Returns:
            AST node at line or None
        """
        if self.language == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if getattr(node, 'lineno', None) == line:
                        return self._python_ast_to_dict(node)
            except SyntaxError:
                pass
        
        return None
    
    def get_all_functions(self, code: str, language: str = "python") -> List[Dict[str, Any]]:
        """
        Get all functions in code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            List of function information
        """
        if language == "python":
            try:
                tree = ast.parse(code)
                functions = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append({
                            "name": node.name,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args],
                            "decorators": [d.id if isinstance(d, ast.Name) else str(d) 
                                          for d in node.decorator_list]
                        })
                
                return functions
            except SyntaxError:
                return []
        
        return []


def parse_ast(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Convenience function to parse code into AST.
    
    Args:
        code: Source code
        language: Programming language
        
    Returns:
        AST as dictionary
    """
    parser = ASTParser()
    return parser.parse(code, language)
