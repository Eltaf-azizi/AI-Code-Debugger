import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Configuration settings for the application.
    Reads from environment variables.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.5"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    
    # Theme settings
    DEFAULT_THEME: str = os.getenv("DEFAULT_THEME", "dark")
    
    # Supported languages
    SUPPORTED_LANGUAGES = [
        "python", "javascript", "typescript", "java", "cpp", "c", 
        "csharp", "go", "rust", "ruby", "php", "swift", "kotlin",
        "sql", "html", "css", "json", "yaml", "bash", "powershell"
    ]
    
    # Validation
    @property
    def is_configured(self):
        return bool(self.OPENAI_API_KEY)
    
    @property
    def is_gpt4(self):
        return "gpt-4" in self.MODEL_NAME.lower()

settings = Settings()
