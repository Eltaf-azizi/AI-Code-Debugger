# AI Code Assistant - Refactoring Plan

## Current State Analysis

### Existing Project Structure
```
AI Code Debugger/
├── main.py                 # Streamlit entry point
├── src/
│   ├── core/
│   │   ├── ai_engine.py   # CodeAnalyzer, DebuggingSession, AnalysisResult
│   │   └── prompts.py     # PromptTemplates (8 action prompts)
│   ├── ui/
│   │   ├── components.py   # Streamlit UI components
│   │   └── layout.py      # Page layouts
│   └── utils/
│       └── config.py      # Configuration settings
├── tests/
│   └── test_engine.py     # Unit tests
└── requirements.txt
```

### Current Capabilities
- **Actions**: Explain, Debug, Optimize, Security, Refactor, Generate Tests, Document, Review
- **Language Support**: Auto-detection + manual specification
- **Session Management**: DebuggingSession with history tracking
- **AI Integration**: OpenAI GPT models via Chat Completions API
- **UI**: Streamlit-based interface

### What Can Be Migrated
| Component | Migration Potential |
|-----------|---------------------|
| `src/core/ai_engine.py` | High - Core logic can become `app/services/ai_service.py` |
| `src/core/prompts.py` | High - Can become `app/services/prompt_templates.py` |
| `src/utils/config.py` | High - Can become `app/config.py` with enhancements |
| `src/ui/layout.py` | Medium - Can be adapted for FastAPI + frontend |
| `src/ui/components.py` | Medium - Can be adapted for frontend |

---

## Target Architecture

### Proposed Structure
```
ai-code-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Enhanced configuration
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # API dependencies
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── summarize.py    # Code summarization endpoint
│   │       ├── debug.py       # Debugging endpoint
│   │       ├── explain.py     # Code explanation endpoint
│   │       ├── optimize.py    # Optimization endpoint
│   │       ├── security.py    # Security analysis endpoint
│   │       └── health.py      # Health check endpoint
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py      # Core AI interaction
│   │   ├── summarizer_service.py
│   │   ├── debugger_service.py
│   │   ├── improvement_service.py
│   │   └── prompt_templates.py # Migrated from prompts.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chunking.py        # Code chunking for large files
│   │   ├── tokenizer.py       # Token counting & limits
│   │   ├── language_detector.py # Language detection
│   │   └── error_parser.py    # Parse syntax errors
│   │
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── python_analyzer.py # Static analysis for Python
│   │   ├── js_analyzer.py     # Static analysis for JavaScript
│   │   ├── security_scanner.py # Security vulnerability detection
│   │   └── ast_parser.py      # AST-based analysis
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py  # Pydantic request schemas
│   │   └── response_models.py # Pydantic response schemas
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py      # Database connection
│   │   └── crud.py           # Database operations
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py         # Logging configuration
│       ├── exceptions.py     # Custom exceptions
│       └── helpers.py        # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_summarizer.py
│   ├── test_debugger.py
│   └── test_api.py
│
├── frontend/                  # Optional React/Vue frontend
│
├── scripts/
│   ├── seed_db.py
│   └── run_local.sh
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
├── .env.example
└── README.md
```

---

