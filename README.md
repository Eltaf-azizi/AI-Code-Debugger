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
├── app/                    # Main application
│   ├── api/               # API routes
│   │   └── routes/        # Endpoint definitions
│   ├── analyzers/         # Static code analyzers
│   ├── core/              # Core utilities
│   ├── database/          # Database operations
│   ├── models/            # Pydantic models
│   ├── services/          # Business logic
│   └── utils/             # Helper functions
├── frontend/              # Next.js frontend
│   └── src/
│       ├── components/    # React components
│       ├── pages/         # Next.js pages
│       └── services/      # API services
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── docker/                 # Docker configuration
└── requirements.txt       # Python dependencies
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
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `MODEL_NAME` | AI model to use | `gpt-4` |
| `TEMPERATURE` | AI creativity | `0.5` |
| `MAX_TOKENS` | Max response tokens | `4000` |
| `DATABASE_URL` | Database connection | SQLite |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for any purpose.

---

Built with ❤️ using FastAPI, Next.js, and OpenAI
