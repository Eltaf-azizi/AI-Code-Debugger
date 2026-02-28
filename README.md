<h1 align="center">🔍 Advanced AI Code Debugger</h1>

A professional, feature-rich AI-powered code analysis tool built with Streamlit and OpenAI GPT models.

## ✨ Features

### Core Analysis
- **🐛 Smart Debugging** - Detect and fix bugs with detailed explanations
- **🔒 Security Analysis** - Identify vulnerabilities using OWASP guidelines
- **⚡ Performance Optimization** - Improve code efficiency and speed
- **🔄 Code Refactoring** - Apply design patterns and best practices


### Documentation & Testing
- **🧪 Test Generation** - Generate comprehensive unit tests
- **📝 Auto-Documentation** - Create detailed docstrings and comments
- **👀 Code Review** - Get professional code review feedback

### Advanced Features
- **🌐 Multi-Language Support** - Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- **📁 File Upload** - Upload single or multiple files for analysis
- **📜 Session History** - Track and revisit your analyses
- **🎨 Modern UI** - Beautiful dark theme with gradient effects

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=sk-your-key-here`

3. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## 📖 Usage

1. Open the application in your browser (http://localhost:8501)
2. Enter your OpenAI API key in the sidebar (or use .env)
3. Select the programming language (or use auto-detect)
4. Choose an action (Explain, Debug, Optimize, Security, etc.)
5. Paste your code or upload a file
6. Click "Run Analysis" to get AI-powered insights

## 🎯 Actions

| Action | Description |
|--------|-------------|
| ✨ Explain | Understand what the code does |
| 🐛 Debug | Find and fix bugs |
| 🚀 Optimize | Improve performance |
| 🛡️ Security | Check for vulnerabilities |
| 🔄 Refactor | Improve code structure |
| 🧪 Test | Generate unit tests |
| 📝 Docs | Generate documentation |
| 👀 Review | Comprehensive code review |

## 🛠️ Configuration

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key
- `MODEL_NAME` - AI model to use (default: gpt-4)
- `TEMPERATURE` - Response creativity (0.0-1.0)
- `MAX_TOKENS` - Maximum response length

### Supported Languages
Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, SQL, HTML, CSS, and more.
