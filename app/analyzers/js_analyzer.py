"""
JavaScript Analyzer
Static analysis for JavaScript/TypeScript code
"""
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class JSFunction:
    """Information about a JavaScript function."""
    name: str
    line_number: int
    params: List[str]
    is_arrow: bool = False
    is_async: bool = False


@dataclass
class JSClass:
    """Information about a JavaScript class."""
    name: str
    line_number: int
    methods: List[str]
    extends: Optional[str] = None


class JavaScriptAnalyzer:
    """
    Static analyzer for JavaScript/TypeScript code.
    Uses regex patterns to extract code structure.
    """
    
    def __init__(self):
        """Initialize JavaScript analyzer."""
        self.functions: List[JSFunction] = []
        self.classes: List[JSClass] = []
        self.imports: List[str] = []
        self.exports: List[str] = []
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """
        Analyze JavaScript code.
        
        Args:
            code: JavaScript source code
            
        Returns:
            Analysis results
        """
        lines = code.split('\n')
        
        # Extract functions
        self._extract_functions(code, lines)
        
        # Extract classes
        self._extract_classes(code, lines)
        
        # Extract imports/exports
        self._extract_imports_exports(code)
        
        return {
            "functions": [f.__dict__ for f in self.functions],
            "classes": [c.__dict__ for c in self.classes],
            "imports": self.imports,
            "exports": self.exports,
            "metrics": self._calculate_metrics()
        }
    
    def _extract_functions(self, code: str, lines: List[str]) -> None:
        """Extract function definitions."""
        # Regular function: function name(...)
        func_pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, code):
            name = match.group(1)
            params = [p.strip() for p in match.group(2).split(',') if p.strip()]
            line = code[:match.start()].count('\n') + 1
            
            self.functions.append(JSFunction(
                name=name,
                line_number=line,
                params=params
            ))
        
        # Arrow functions: const name = (...) => or name: (...) =>
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:\([^)]*\)|[^=])\s*=>'
        for match in re.finditer(arrow_pattern, code):
            name = match.group(1)
            line = code[:match.start()].count('\n') + 1
            
            self.functions.append(JSFunction(
                name=name,
                line_number=line,
                params=[],
                is_arrow=True
            ))
        
        # Method definitions in classes
        method_pattern = r'(\w+)\s*\(([^)]*)\)\s*\{'
        for match in re.finditer(method_pattern, code):
            # Skip if it's not inside a class context
            name = match.group(1)
            if name not in ['if', 'for', 'while', 'switch', 'else', 'try', 'catch']:
                params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                line = code[:match.start()].count('\n') + 1
                
                # Check if it's new
                if not any(f.name == name and f.line_number == line for f in self.functions):
                    self.functions.append(JSFunction(
                        name=name,
                        line_number=line,
                        params=params
                    ))
    
    def _extract_classes(self, code: str, lines: List[str]) -> None:
        """Extract class definitions."""
        # class Name { ... }
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        for match in re.finditer(class_pattern, code):
            name = match.group(1)
            extends = match.group(2)
            line = code[:match.start()].count('\n') + 1
            
            # Extract methods
            class_code = self._get_class_body(code, match.end())
            methods = re.findall(r'(\w+)\s*\([^)]*\)\s*\{', class_code)
            
            self.classes.append(JSClass(
                name=name,
                line_number=line,
                methods=methods,
                extends=extends
            ))
    
    def _get_class_body(self, code: str, start: int) -> str:
        """Extract class body."""
        depth = 1
        i = start
        while i < len(code) and depth > 0:
            if code[i] == '{':
                depth += 1
            elif code[i] == '}':
                depth -= 1
            i += 1
        return code[start:i]
    
    def _extract_imports_exports(self, code: str) -> None:
        """Extract import and export statements."""
        # ES6 imports
        import_pattern = r'import\s+(?:{[^}]+}|[\w]+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, code):
            self.imports.append(match.group(1))
        
        # require
        require_pattern = r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        for match in re.finditer(require_pattern, code):
            self.imports.append(match.group(1))
        
        # exports
        export_pattern = r'export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)'
        for match in re.finditer(export_pattern, code):
            self.exports.append(match.group(1))
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate code metrics."""
        return {
            "total_functions": len(self.functions),
            "total_classes": len(self.classes),
            "total_imports": len(self.imports),
            "total_exports": len(self.exports)
        }


def analyze_javascript(code: str) -> Dict[str, Any]:
    """
    Convenience function to analyze JavaScript code.
    
    Args:
        code: JavaScript source code
        
    Returns:
        Analysis results
    """
    analyzer = JavaScriptAnalyzer()
    return analyzer.analyze(code)
