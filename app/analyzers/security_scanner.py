"""
Security Scanner
Detect security vulnerabilities in code (OWASP Top 10)
"""
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecurityFinding:
    """Security vulnerability finding."""
    line: int
    severity: str  # Critical, High, Medium, Low
    category: str  # OWASP category
    description: str
    suggestion: str


class SecurityScanner:
    """
    Security vulnerability scanner.
    Detects common security issues based on OWASP Top 10.
    """
    
    # Vulnerability patterns with severity
    PATTERNS = {
        # SQL Injection
        "sql_injection": [
            (r'execute\s*\(\s*["\'].*%s', "High", "SQL Injection", 
             "Use parameterized queries instead of string formatting"),
            (r'exec\s*\(\s*["\'].*%s', "Critical", "SQL Injection",
             "Never use exec with user input"),
            (r'cursor\.execute\s*\([^,]+\+', "High", "SQL Injection",
             "Use parameterized queries"),
        ],
        # Command Injection
        "command_injection": [
            (r'os\.system\s*\(', "High", "Command Injection",
             "Use subprocess with shell=False"),
            (r'subprocess\.call\s*\([^,]+,\s*shell\s*=\s*True', "High", "Command Injection",
             "Set shell=False"),
            (r'eval\s*\(', "Critical", "Code Injection",
             "Avoid eval with user input"),
            (r'exec\s*\(', "Critical", "Code Injection",
             "Avoid exec with user input"),
        ],
        # Path Traversal
        "path_traversal": [
            (r'open\s*\([^,]*\+', "Medium", "Path Traversal",
             "Validate and sanitize file paths"),
            (r'os\.path\.join\s*\([^,]*\+', "Medium", "Path Traversal",
             "Validate path components"),
        ],
        # XSS
        "xss": [
            (r'innerHTML\s*=', "High", "XSS",
             "Use textContent instead of innerHTML"),
            (r'document\.write\s*\(', "Medium", "XSS",
             "Use DOM manipulation methods"),
        ],
        # Hardcoded Secrets
        "hardcoded_secrets": [
            (r'password\s*=\s*["\'][^"\']+["\']', "High", "Hardcoded Secrets",
             "Use environment variables for secrets"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "High", "Hardcoded Secrets",
             "Use environment variables for API keys"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "High", "Hardcoded Secrets",
             "Use environment variables for secrets"),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', "Medium", "Hardcoded Secrets",
             "Use environment variables for tokens"),
        ],
        # Weak Cryptography
        "weak_crypto": [
            (r'md5\s*\(', "Medium", "Weak Cryptography",
             "Use SHA-256 or stronger"),
            (r'sha1\s*\(', "Medium", "Weak Cryptography",
             "Use SHA-256 or stronger"),
            (r'DES\s*\(', "Medium", "Weak Cryptography",
             "Use AES-256"),
        ],
        # Insecure Random
        "insecure_random": [
            (r'random\.random\s*\(', "Low", "Insecure Random",
             "Use secrets module for cryptographic randomness"),
        ],
        # Unsafe YAML
        "unsafe_yaml": [
            (r'yaml\.load\s*\([^,)]*\)', "High", "Unsafe YAML",
             "Use yaml.safe_load"),
        ],
        # Debug Mode
        "debug_mode": [
            (r'DEBUG\s*=\s*True', "Medium", "Debug Mode",
             "Disable debug in production"),
        ],
        # Insecure Dependencies (detection via import)
        "insecure_imports": [
            (r'import\s+pickle', "Medium", "Insecure Deserialization",
             "Use JSON for data serialization"),
        ],
    }
    
    def __init__(self):
        """Initialize security scanner."""
        self.findings: List[SecurityFinding] = []
    
    def scan(self, code: str) -> Dict[str, Any]:
        """
        Scan code for security vulnerabilities.
        
        Args:
            code: Source code to scan
            
        Returns:
            Scan results with findings
        """
        self.findings = []
        lines = code.split('\n')
        
        # Check each pattern
        for category, patterns in self.PATTERNS.items():
            for pattern, severity, vuln_type, suggestion in patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        self.findings.append(SecurityFinding(
                            line=i,
                            severity=severity,
                            category=vuln_type,
                            description=f"Potential {vuln_type} in line {i}",
                            suggestion=suggestion
                        ))
        
        return self._format_results()
    
    def _format_results(self) -> Dict[str, Any]:
        """Format scan results."""
        # Group by severity
        by_severity = {
            "Critical": [],
            "High": [],
            "Medium": [],
            "Low": []
        }
        
        for finding in self.findings:
            by_severity[finding.severity].append({
                "line": finding.line,
                "category": finding.category,
                "description": finding.description,
                "suggestion": finding.suggestion
            })
        
        return {
            "total_findings": len(self.findings),
            "by_severity": by_severity,
            "findings": [
                {
                    "line": f.line,
                    "severity": f.severity,
                    "category": f.category,
                    "description": f.description,
                    "suggestion": f.suggestion
                }
                for f in self.findings
            ]
        }
    
    def get_risk_score(self) -> float:
        """Calculate overall risk score (0-100)."""
        if not self.findings:
            return 0.0
        
        severity_weights = {
            "Critical": 25,
            "High": 15,
            "Medium": 5,
            "Low": 1
        }
        
        score = sum(severity_weights[f.severity] for f in self.findings)
        return min(score, 100)


def scan_security(code: str) -> Dict[str, Any]:
    """
    Convenience function to scan code for security issues.
    
    Args:
        code: Source code
        
    Returns:
        Security scan results
    """
    scanner = SecurityScanner()
    return scanner.scan(code)
