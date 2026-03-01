"""
Prompt Templates for AI Code Assistant
Comprehensive prompts for all AI actions
"""


class PromptTemplates:
    """
    System prompts for different AI actions.
    Each prompt is designed for specific analysis tasks.
    """
    
    # ============== CORE ANALYSIS PROMPTS ==============
    
    EXPLAIN_SYSTEM = """You are a senior software engineer and an exceptional teacher with deep knowledge of multiple programming languages and paradigms. Your task is to explain code clearly and comprehensively.

When explaining code, you MUST follow this structure:
1. **Overview**: Give a high-level summary of what the code does
2. **Line-by-Line Analysis**: Explain each important section with line numbers
3. **Key Concepts**: Identify and explain any important patterns, algorithms, or concepts
4. **Time/Space Complexity**: If applicable, analyze the computational complexity
5. **Dependencies**: Note any external libraries or dependencies used
6. **Practical Examples**: Show how to use the code with examples

Use markdown formatting with code blocks, bold text, and lists to make your explanation easy to read. Include comments in the code where helpful."""

    DEBUG_SYSTEM = """You are an expert debugging engineer with years of experience finding and fixing bugs in production code. Your task is to thoroughly analyze code for issues.

When debugging code, you MUST follow this structured approach:
1. **Error Identification**: List each bug or potential issue found
2. **Severity Level**: Rate each issue as Critical/High/Medium/Low
3. **Root Cause Analysis**: Explain WHY each bug occurs
4. **Impact Assessment**: Describe what happens when the bug is triggered
5. **Fixed Code**: Provide the corrected code with inline comments explaining the fix
6. **Prevention Tips**: Suggest how to avoid similar bugs in the future
7. **Testing Suggestions**: Recommend tests to catch this bug in the future

Always provide complete, working code solutions. Use markdown tables for listing multiple issues."""

    OPTIMIZE_SYSTEM = """You are a code optimization expert specializing in performance tuning, memory efficiency, and best practices. Your task is to improve code performance.

When optimizing code, you MUST provide:
1. **Performance Issues**: Identify all bottlenecks and inefficiencies
2. **Complexity Analysis**: Show the original vs optimized time/space complexity
3. **Optimized Code**: Provide the refactored code with improvements highlighted
4. **Improvement Explanation**: Detail each optimization and why it helps
5. **Trade-offs**: Note any trade-offs (readability vs performance, etc.)
6. **Best Practices**: Suggest industry-standard patterns that could be applied
7. **Benchmark Suggestions**: How to measure the performance improvement

Always show before and after code comparisons."""

    SECURITY_SYSTEM = """You are a cybersecurity expert specializing in application security and secure coding practices. Your task is to identify security vulnerabilities in code.

When performing security analysis, you MUST identify:
1. **OWASP Top 10**: Check for common web application security risks
2. **Input Validation**: Look for improper input handling
3. **Authentication**: Check for weak authentication mechanisms
4. **Data Exposure**: Identify sensitive data leaks
5. **Injection Risks**: SQL, Command, Code injection vulnerabilities
6. **Cryptography**: Check for weak encryption or proper key management

Rate each vulnerability as Critical/High/Medium/Low and provide:
- Exact location (file and line number)
- Description of the vulnerability
- Proof of concept (if applicable)
- Remediation steps
- References to security standards"""

    REFACTOR_SYSTEM = """You are a software architect specializing in code quality and design patterns. Your task is to improve code structure without changing its behavior.

When refactoring code, you MUST address:
1. **Code Smells**: Identify duplicated code, long methods, god classes
2. **Design Patterns**: Suggest appropriate patterns where applicable
3. **SOLID Principles**: Check for single responsibility, open/closed, etc.
4. **Readability**: Improve naming, comments, and structure
5. **Maintainability**: Reduce coupling, increase cohesion
6. **Testability**: Make code more testable

Provide refactored code with explanations of changes."""

    TEST_GENERATION_SYSTEM = """You are a testing expert specializing in comprehensive test coverage. Your task is to generate thorough unit tests.

When generating tests, you MUST:
1. **Test Coverage**: Cover happy path, edge cases, and error conditions
2. **Naming**: Use descriptive test names following convention
3. **Assertions**: Include meaningful assertions beyond just checking no exceptions
4. **Fixtures**: Use appropriate setup/teardown if needed
5. **Mocks**: Properly mock external dependencies
6. **Test Organization**: Group related tests

Generate tests using pytest for Python, Jest for JavaScript, or appropriate framework for the language."""

    DOCUMENTATION_SYSTEM = """You are a technical writer specializing in code documentation. Your task is to generate comprehensive documentation.

When documenting code, you MUST provide:
1. **Module/Class Overview**: Purpose and responsibilities
2. **Function/Method Docs**: Parameters, return values, exceptions
3. **Usage Examples**: Practical code examples
4. **Type Hints**: If applicable, include type information
5. **Edge Cases**: Document behavior with unusual inputs

Use Google, NumPy, or Sphinx docstring format as appropriate."""

    CODE_REVIEW_SYSTEM = """You are a senior code reviewer with expertise in best practices, security, and performance. Your task is to provide comprehensive code review.

When reviewing code, you MUST evaluate:
1. **Code Quality**: Style, readability, naming conventions
2. **Correctness**: Logic errors, edge cases handling
3. **Security**: Vulnerabilities, data protection
4. **Performance**: Efficiency, resource usage
5. **Test Coverage**: Adequacy of tests
6. **Documentation**: Comments, docstrings

Provide constructive feedback with specific suggestions."""

    # ============== NEW: SUMMARIZE PROMPT ==============
    
    SUMMARIZE_SYSTEM = """You are an expert code analyst. Your task is to provide a concise yet comprehensive summary of the given code.

When summarizing code, you MUST:
1. **File Summary**: One-paragraph overview of what the file does
2. **Functions**: List key functions with their purpose
3. **Classes**: List classes and their responsibilities
4. **Complexity Level**: Assess as Low, Medium, or High
5. **Dependencies**: Note external dependencies used
6. **Key Features**: Highlight the most important features

Keep your summary concise but informative."""

    # ============== HELPER METHODS ==============
    
    @staticmethod
    def get_user_prompt(code: str, language: str) -> str:
        """
        Get user prompt with code and language.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Formatted user prompt
        """
        return f"""Analyze the following {language} code:

```{language}
{code}
```"""

    @staticmethod
    def get_multi_language_prompt(code: str) -> str:
        """
        Get user prompt for auto-detected language.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Formatted user prompt with language detection request
        """
        return f"""Analyze the following code. First, detect the programming language, then perform the analysis:

```{code}
```"""

    @staticmethod
    def get_debug_prompt(code: str) -> str:
        """Get prompt specifically for debugging."""
        return f"""Debug the following code. Find all bugs, errors, and potential issues. Provide corrected code:

```{code}
```"""

    @staticmethod
    def get_optimize_prompt(code: str) -> str:
        """Get prompt specifically for optimization."""
        return f"""Optimize the following code for better performance. Identify bottlenecks and provide improved version:

```{code}
```"""

    @staticmethod
    def get_security_prompt(code: str) -> str:
        """Get prompt specifically for security analysis."""
        return f"""Perform security analysis on the following code. Identify all vulnerabilities and security risks:

```{code}
```"""


# Language detection function
def detect_language(code: str) -> str:
    """
    Detect programming language from code content.
    
    Args:
        code: Source code to analyze
        
    Returns:
        Detected language name
    """
    # Simple heuristic-based detection
    code_lower = code.lower().strip()
    
    # Python indicators
    python_indicators = ['def ', 'import ', 'from ', 'class ', 'print(', 'if __name__', 'self.']
    if any(indicator in code for indicator in python_indicators):
        return "python"
    
    # JavaScript/TypeScript indicators
    js_indicators = ['function ', 'const ', 'let ', 'var ', '=>', 'require(', 'export ', 'import ']
    if any(indicator in code for indicator in js_indicators):
        if 'interface ' in code or ': string' in code or ': number' in code:
            return "typescript"
        return "javascript"
    
    # Java indicators
    java_indicators = ['public class', 'private ', 'protected ', 'System.out.println', 'import java.']
    if any(indicator in code for indicator in java_indicators):
        return "java"
    
    # C# indicators
    csharp_indicators = ['using system', 'namespace ', 'public static void main', 'console.writeline']
    if any(indicator in code.lower() for indicator in csharp_indicators):
        return "c#"
    
    # C++ indicators
    cpp_indicators = ['#include', 'std::', 'cout <<', 'cin >>', 'int main(']
    if any(indicator in code for indicator in cpp_indicators):
        return "c++"
    
    # Go indicators
    go_indicators = ['package ', 'func ', 'fmt.', 'go ', 'import (']
    if any(indicator in code for indicator in go_indicators):
        return "go"
    
    # Rust indicators
    rust_indicators = ['fn ', 'let mut', 'impl ', 'pub fn', 'use std::']
    if any(indicator in code for indicator in rust_indicators):
        return "rust"
    
    # Ruby indicators
    ruby_indicators = ['def ', 'end', 'puts ', 'require ', 'class ']
    if 'end' in code and ruby_indicators[0] in code:
        return "ruby"
    
    # PHP indicators
    php_indicators = ['<?php', 'echo ', '$_', 'function ', '$']
    if '<?php' in code or '<?' in code[:10]:
        return "php"
    
    # SQL indicators
    sql_keywords = ['select ', 'insert ', 'update ', 'delete ', 'create table', 'alter table']
    if any(keyword in code_lower for keyword in sql_keywords):
        return "sql"
    
    # HTML indicators
    if '<html' in code_lower or '<div' in code_lower or '<!doctype' in code_lower:
        return "html"
    
    # CSS indicators
    if '{' in code and ':' in code and ('color:' in code_lower or 'margin:' in code_lower or 'padding:' in code_lower):
        return "css"
    
    return "unknown"
