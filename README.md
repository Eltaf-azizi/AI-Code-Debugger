# 🎯 AI Code Assistant

An intelligent AI-powered system that understands, analyzes, summarizes, debugs, and improves source code. Built with modern AI integration and best practices.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Capabilities

| Action | Description |
|--------|-------------|
| ✨ **Explain** | Understand what the code does with detailed explanations |
| 🐛 **Debug** | Find and fix bugs with precise error locations and corrections |
| 🚀 **Optimize** | Improve performance with algorithmic optimizations |
| 🛡️ **Security** | Check for vulnerabilities (OWASP Top 10) |
| 🔄 **Refactor** | Improve code structure and apply design patterns |
| 📝 **Summarize** | Get concise file summaries with complexity analysis |
| 🧪 **Test** | Generate comprehensive unit tests |
| 👀 **Review** | Comprehensive code review with best practices |

### Technical Highlights

- 🤖 **AI-Powered**: Leverages OpenAI GPT models for intelligent analysis
- 📊 **Structured Outputs**: Always returns valid JSON for easy integration
- 🔍 **Static Analysis**: Built-in AST parsing for Python and JavaScript
- 🛡️ **Security Scanner**: Detects OWASP Top 10 vulnerabilities
- 📈 **Performance Analysis**: Identifies bottlenecks and optimization opportunities
- 🌍 **Multi-Language**: Supports Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more

---

## 📁 Project Structure

```
AI Code Assistant/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration management
│   │
│   ├── api/                 # API routes
│   │   ├── dependencies.py  # Shared dependencies
│   │   └── routes/          # API endpoints
│   │       ├── health.py    # Health check
│   │       ├── summarize.py # Summarization
│   │       ├── debug.py     # Debugging
│   │       ├── explain.py   # Code explanation
│   │       ├── optimize.py  # Optimization
│   │       └── security.py  # Security analysis
│   │
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # OpenAI integration
│   │   ├── summarizer_service.py
│   │   ├── debugger_service.py
│   │   ├── improvement_service.py
│   │   └── prompt_templates.py
│   │
│   ├── core/                # Core utilities
│   │   ├── chunking.py     # Code chunking for large files
│   │   ├── tokenizer.py    # Token counting
│   │   ├── language_detector.py
│   │   └── error_parser.py
│   │
│   ├── analyzers/           # Static analysis
│   │   ├── python_analyzer.py  # Python AST analysis
│   │   ├── js_analyzer.py     # JavaScript analysis
│   │   ├── security_scanner.py # Vulnerability detection
│   │   └── ast_parser.py      # Generic AST parsing
│   │
│   ├── models/              # Pydantic models
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   ├── database/            # Database layer
│   │   ├── connection.py
│   │   └── crud.py
│   │
│   └── utils/               # Utilities
│       ├── logger.py
│       ├── exceptions.py
│       └── helpers.py
│
├── tests/                   # Unit tests
├── docker/                  # Docker configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- OpenAI API Key

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd AI-Code-Assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Run the API**
```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

6. **Open documentation**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `MODEL_NAME` | AI model to use | `gpt-4` |
| `TEMPERATURE` | Response creativity (0.0-1.0) | `0.5` |
| `MAX_TOKENS` | Maximum response length | `4000` |
| `DATABASE_URL` | Database connection string | SQLite |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## 📡 API Endpoints

### Health Check

```bash
GET /api/v1/health
```

### Summarize Code

```bash
POST /api/v1/summarize
{
  "code": "def hello():\n    print('Hello')",
  "language": "python"
}
```

**Response:**
```json
{
  "success": true,
  "file_summary": "This function prints hello...",
  "functions": [{"name": "hello", "summary": "Prints hello"}],
  "classes": [],
  "complexity_level": "Low"
}
```

### Debug Code

```bash
POST /api/v1/debug
{
  "code": "def divide(a, b):\n    return a / b",
  "language": "python"
}
```

### Security Analysis

```bash
POST /api/v1/security
{
  "code": "query = f'SELECT * FROM users WHERE id = {user_input}'",
  "language": "python"
}
```

### All Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/summarize` | POST | Summarize code |
| `/api/v1/debug` | POST | Debug code |
| `/api/v1/explain` | POST | Explain code |
| `/api/v1/optimize` | POST | Optimize code |
| `/api/v1/security` | POST | Security analysis |

---

## 📊 Output Schemas

### A. Code Summarization

```json
{
  "file_summary": "This file handles user authentication...",
  "functions": [
    {"name": "login_user", "summary": "Authenticates user..."}
  ],
  "classes": [
    {"name": "AuthService", "summary": "Handles authentication..."}
  ],
  "complexity_level": "Medium"
}
```

### B. Debugging Output

```json
{
  "syntax_errors": [
    {"line": 12, "error": "Missing colon", "fix": "Add ':'"}
  ],
  "logical_issues": [
    {"line": 24, "issue": "Division by zero", "suggestion": "Check denominator"}
  ],
  "corrected_code": "..."
}
```

### C. Security Analysis

```json
{
  "security_risks": [
    {
      "line": 18,
      "risk": "SQL Injection",
      "severity": "High",
      "fix": "Use parameterized queries"
    }
  ],
  "risk_score": 75
}
```

### D. Code Optimization

```json
{
  "performance_suggestions": [
    {
      "line": 30,
      "issue": "O(n²) complexity",
      "improvement": "Use dictionary for O(1) lookup"
    }
  ],
  "refactor_suggestions": [
    {"area": "function login", "suggestion": "Split into smaller functions"}
  ]
}
```

---

## 🏆 Success Criteria

### Functional Requirements

- ✅ Works for Python and JavaScript
- ✅ Handles files up to 2,000+ lines
- ✅ Returns structured JSON 95% of the time
- ✅ Detects syntax errors reliably

### Technical Requirements

- ✅ Clean modular codebase
- ✅ Each service independent
- ✅ Unit tests for all services
- ✅ API integration tests

### AI Quality

- ✅ Summary is accurate
- ✅ Bugs explained clearly
- ✅ No hallucinated errors
- ✅ Fix suggestions compile successfully

---

## 🐳 Docker

```bash
# Build and run with Docker
docker build -t ai-code-assistant -f docker/Dockerfile .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai-code-assistant

# Or use Docker Compose
docker-compose -f docker/docker-compose.yml up
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

---

## 🔒 Security

- Your code is sent to OpenAI for processing
- No code is stored on any server
- API key is kept local
- Use environment variables for secrets

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 🧠 What This Project Proves

If done properly, this project proves:

- ✅ Understanding of AI integration
- ✅ Backend architecture design
- ✅ Static analysis implementation
- ✅ Building scalable systems
- ✅ Thinking beyond simple CRUD apps

This is what separates beginners from real builders. 🚀
