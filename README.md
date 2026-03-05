# 🔍 AI Code Assistant

A powerful AI-powered code analysis, debugging, and optimization tool built with FastAPI and Next.js.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)

## ✨ Features

- **🤖 AI-Powered Analysis** - Uses GPT-4 for intelligent code analysis
- **🐛 Smart Debugging** - Find and fix bugs with AI assistance
- **🔒 Security Scanning** - Detect security vulnerabilities (OWASP Top 10)
- **⚡ Performance Optimization** - Get optimization suggestions
- **📝 Code Summarization** - Understand code quickly
- **💡 Code Explanation** - Learn what code does
- **🧪 Test Generation** - Auto-generate unit tests

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- OpenAI API Key

### Backend Setup

```bash
# Navigate to project directory
cd ai-code-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the API server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup (Optional)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
ai-code-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # API dependencies
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── summarize.py    # Code summarization endpoint
│   │       ├── debug.py        # Debugging endpoint
│   │       ├── explain.py      # Code explanation endpoint
│   │       ├── optimize.py     # Optimization endpoint
│   │       ├── security.py     # Security analysis endpoint
│   │       └── health.py       # Health check endpoint
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # Core AI interaction
│   │   ├── summarizer_service.py
│   │   ├── debugger_service.py
│   │   ├── improvement_service.py
│   │   └── prompt_templates.py # AI prompt templates
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chunking.py         # Code chunking for large files
│   │   ├── tokenizer.py        # Token counting & limits
│   │   ├── language_detector.py
│   │   └── error_parser.py     # Parse syntax errors
│   │
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── python_analyzer.py  # Static analysis for Python
│   │   ├── js_analyzer.py      # Static analysis for JavaScript
│   │   ├── security_scanner.py # Security vulnerability detection
│   │   └── ast_parser.py       # AST-based analysis
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db_models.py        # SQLAlchemy models
│   │   ├── request_models.py   # Pydantic request schemas
│   │   └── response_models.py # Pydantic response schemas
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Database connection
│   │   ├── crud.py            # Database operations
│   │   └── migrations/
│   │       └── __init__.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging configuration
│       ├── exceptions.py      # Custom exceptions
│       └── helpers.py         # Utility functions
│
├── frontend/                   # Next.js frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── src/
│       ├── pages/
│       │   ├── _app.js
│       │   ├── _document.js
│       │   └── index.js
│       ├── components/
│       │   ├── CodeEditor.js
│       │   └── ResultViewer.js
│       ├── services/
│       │   └── api.js
│       └── styles/
│           └── globals.css
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_summarizer.py
│   ├── test_debugger.py
│   ├── test_api.py
│   ├── test_ai_service.py
│   ├── test_core.py
│   ├── test_database.py
│   └── test_engine.py
│
├── scripts/                   # Utility scripts
│   ├── seed_db.py
│   └── run_local.sh
│
├── docker/                    # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── src/                       # Legacy Streamlit UI (deprecated)
│   ├── core/
│   │   ├── ai_engine.py
│   │   └── prompts.py
│   ├── ui/
│   │   ├── components.py
│   │   └── layout.py
│   └── utils/
│       └── config.py
│
├── plans/                     # Planning documents
│   └── refactoring_plan.md
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env                       # Environment variables (local)
├── .env.example              # Environment template
├── .gitignore
└── main.py                    # Legacy entry point
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/summarize` | POST | Summarize code |
| `/api/v1/debug` | POST | Debug code |
| `/api/v1/explain` | POST | Explain code |
| `/api/v1/optimize` | POST | Optimize code |
| `/api/v1/security` | POST | Security analysis |

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello\")",
    "language": "python"
  }'
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
cd docker
docker-compose up --build
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=app tests/
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `MODEL_NAME` | AI model to use | `gpt-4` |
| `TEMPERATURE` | AI creativity | `0.5` |
| `MAX_TOKENS` | Max response tokens | `4000` |
| `DATABASE_URL` | Database connection | SQLite |
| `DEBUG` | Debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🏗️ Architecture

### Backend (FastAPI)
The backend is built with FastAPI and follows a modular architecture:
- **API Layer**: REST endpoints for each feature
- **Service Layer**: Business logic and AI integration
- **Core Layer**: Utilities for tokenization, chunking, language detection
- **Analyzer Layer**: Static code analysis for Python and JavaScript
- **Database Layer**: SQLAlchemy ORM for data persistence

### Frontend (Next.js)
The frontend is built with Next.js 14:
- **Components**: CodeEditor, ResultViewer
- **Services**: API client for backend communication
- **Pages**: Main application interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for any purpose.

---

Built with ❤️ using FastAPI, Next.js, and OpenAI
