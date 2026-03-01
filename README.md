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

## 📁 Project Structure

```
AI Code Debugger/
├── main.py                 # Application entry point
├── src/
│   ├── core/
│   │   ├── ai_engine.py   # AI analysis engine
│   │   └── prompts.py     # AI prompt templates
│   ├── ui/
│   │   ├── components.py  # UI components
│   │   └── layout.py     # Layout
│   └── utils/
│       └── config.py     # Configuration
├── tests/                  # Unit tests
│   └── test_engine.py    # Engine tests
├── .streamlit/
│   └── config.toml       # Streamlit config
├── requirements.txt      # Dependencies
└── .env.example         # Environment template
```

## 🔒 Security

- Your code is sent to OpenAI for processing
- No code is stored on any server
- API key is kept local

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
