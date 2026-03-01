"""
Python Analyzer
Static analysis for Python code using AST
"""
import ast
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Information about a Python function."""
    name: str
    line_number: int
    params: List[str]
    complexity: int = 1
    docstring: Optional[str] = None


@dataclass
class ClassInfo:
    """Information about a Python class."""
    name: str
    line_number: int
    methods: List[str]
    base_classes: List[str]
    docstring: Optional[str] = None


class PythonAnalyzer:
    """
    Static analyzer for Python code.
    Uses AST to extract code structure and metrics.
    """
    
    def __init__(self):
        """Initialize Python analyzer."""
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.imports: List[str] = []
        self.errors: List[Dict[str, Any]] = []
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """
        Analyze Python code.
        
        Args:
            code: Python source code
            
        Returns:
            Analysis results
        """
        try:
            tree = ast.parse(code)
            self._extract_info(tree)
            return {
                "functions": [f.__dict__ for f in self.functions],
                "classes": [c.__dict__ for c in self.classes],
                "imports": self.imports,
                "errors": self.errors,
                "metrics": self._calculate_metrics()
            }
        except SyntaxError as e:
            return {
                "error": str(e),
                "syntax_error": {
                    "line": e.lineno,
                    "message": e.msg
                }
            }
    
    def _extract_info(self, tree: ast.AST) -> None:
        """Extract information from AST."""
        for node in ast.walk(tree):
            # Extract imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports.append(node.module)
            
            # Extract functions
            elif isinstance(node, ast.FunctionDef):
                func_info = FunctionInfo(
                    name=node.name,
                    line_number=node.lineno,
                    params=[arg.arg for arg in node.args.args],
                    complexity=self._calculate_complexity(node),
                    docstring=ast.get_docstring(node)
                )
                self.functions.append(func_info)
            
            # Extract classes
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                class_info = ClassInfo(
                    name=node.name,
                    line_number=node.lineno,
                    methods=methods,
                    base_classes=[b.attr if hasattr(b, 'attr') else str(b) for b in node.bases],
                    docstring=ast.get_docstring(node)
                )
                self.classes.append(class_info)
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate code metrics."""
        return {
            "total_functions": len(self.functions),
            "total_classes": len(self.classes),
            "total_imports": len(self.imports),
            "avg_function_complexity": sum(f.complexity for f in self.functions) / max(len(self.functions), 1)
        }
    
    def get_function_at_line(self, code: str, line: int) -> Optional[FunctionInfo]:
        """Get function containing specific line."""
        self.analyze(code)
        for func in self.functions:
            # Simple heuristic: function spans roughly 20 lines
            if func.line_number <= line <= func.line_number + 20:
                return func
        return None


def analyze_python(code: str) -> Dict[str, Any]:
    """
    Convenience function to analyze Python code.
    
    Args:
        code: Python source code
        
    Returns:
        Analysis results
    """
    analyzer = PythonAnalyzer()
    return analyzer.analyze(code)
