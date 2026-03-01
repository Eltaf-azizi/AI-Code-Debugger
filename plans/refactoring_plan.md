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

## Detailed Migration Steps

### Phase 1: Foundation (Step 1-3)

#### Step 1: Create Directory Structure
Create all directories as outlined in target architecture.

#### Step 2: Migrate Configuration
- Move `src/utils/config.py` → `app/config.py`
- Add new settings:
  - `DATABASE_URL`
  - `LOG_LEVEL`
  - `MAX_FILE_SIZE`
  - `CHUNK_SIZE`
  - `CACHE_ENABLED`

#### Step 3: Set Up FastAPI Main Entry
- Create `app/main.py` with FastAPI app
- Include middleware (CORS, logging)
- Register API routes

### Phase 2: Core Services (Step 4-6)

#### Step 4: Create Service Layer
| Service | Source | Purpose |
|---------|--------|---------|
| `ai_service.py` | `ai_engine.py` | OpenAI integration |
| `summarizer_service.py` | New | Code summarization logic |
| `debugger_service.py` | New | Debugging with static analysis |
| `improvement_service.py` | New | Optimization & refactoring |
| `prompt_templates.py` | `prompts.py` | Migrate existing prompts |

#### Step 5: Create Core Utilities
- `chunking.py`: Split large files into manageable chunks
- `tokenizer.py`: Count tokens, enforce limits
- `language_detector.py`: Detect programming language
- `error_parser.py`: Parse Python/JavaScript errors

#### Step 6: Create Language Analyzers
- `python_analyzer.py`: Use `ast` module, pylint integration
- `js_analyzer.py`: Use ESLint, Babel parser
- `security_scanner.py`: Detect OWASP Top 10 vulnerabilities
- `ast_parser.py`: Generic AST traversal

### Phase 3: API & Models (Step 7-9)

#### Step 7: Define Pydantic Models
**Request Models** (`app/models/request_models.py`):
```python
class AnalyzeCodeRequest(BaseModel):
    code: str
    language: Optional[str] = "auto"
    action: str  # summarize, debug, explain, optimize, security
```

**Response Models** (`app/models/response_models.py`):
```python
class SummarizationResponse(BaseModel):
    file_summary: str
    functions: List[FunctionSummary]
    classes: List[ClassSummary]
    complexity_level: str

class DebuggingResponse(BaseModel):
    syntax_errors: List[SyntaxError]
    logical_issues: List[LogicalIssue]
    corrected_code: Optional[str]
```

#### Step 8: Create API Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/summarize` | POST | Summarize code |
| `/api/v1/debug` | POST | Find and fix bugs |
| `/api/v1/explain` | POST | Explain code |
| `/api/v1/optimize` | POST | Optimize performance |
| `/api/v1/security` | POST | Security analysis |
| `/api/v1/health` | GET | Health check |

#### Step 9: Database Setup
- Set up SQLAlchemy connection
- Create CRUD operations for:
  - Analysis history
  - User sessions
  - Code snippets

### Phase 4: Infrastructure (Step 10-14)

#### Step 10: Update Dependencies
New packages needed:
```
fastapi
uvicorn
pydantic
sqlalchemy
python-multipart
```

#### Step 11: Docker Configuration
- Create Dockerfile with Python 3.11
- Set up docker-compose with:
  - API service
  - PostgreSQL database
  - Optional: Redis for caching

#### Step 12: Update Tests
- Create unit tests for each service
- Create API integration tests
- Maintain test coverage > 80%

#### Step 13: Update README
- Document new architecture
- Include output schemas (JSON format)
- Add success criteria
- Include setup instructions

#### Step 14: Verify & Deploy
- Run all tests
- Test API endpoints
- Deploy to cloud (Render/Replit/Vercel)

---

## Output Schemas

### A. Code Summarization
```json
{
  "file_summary": "This file handles user authentication...",
  "functions": [{"name": "login_user", "summary": "..."}],
  "classes": [{"name": "AuthService", "summary": "..."}],
  "complexity_level": "Medium"
}
```

### B. Debugging Output
```json
{
  "syntax_errors": [{"line": 12, "error": "...", "fix": "..."}],
  "logical_issues": [{"line": 24, "issue": "...", "suggestion": "..."}],
  "corrected_code": "..."
}
```

### C. Security Analysis
```json
{
  "security_risks": [
    {"line": 18, "risk": "SQL Injection", "severity": "High", "fix": "..."}
  ]
}
```

### D. Code Improvement
```json
{
  "performance_suggestions": [{"line": 30, "issue": "O(n^2)", "improvement": "..."}],
  "refactor_suggestions": [{"area": "function", "suggestion": "..."}]
}
```

---

## Success Criteria

| Category | Metric |
|----------|--------|
| Functional | Works for Python & JavaScript |
| Functional | Handles files up to 2,000+ lines |
| Functional | Returns structured JSON 95% of time |
| Technical | Clean modular codebase |
| Technical | Each service independent |
| AI Quality | Summary is accurate |
| AI Quality | Bugs explained clearly |
| AI Quality | No hallucinated errors |

---

## Migration Priority

```
HIGH PRIORITY (Migrate First):
├── app/config.py
├── app/services/ai_service.py
├── app/services/prompt_templates.py
└── app/core/language_detector.py

MEDIUM PRIORITY (Next Phase):
├── app/api/routes/*
├── app/models/*
├── app/core/* (chunking, tokenizer, error_parser)
└── app/analyzers/*

LOW PRIORITY (Later):
├── app/database/*
├── docker/*
└── frontend/
```

---

## Notes

1. **Backward Compatibility**: Keep old Streamlit UI working during migration
2. **Incremental Changes**: Migrate one feature at a time
3. **Testing**: Write tests before migrating each component
4. **Documentation**: Update README after each major change
