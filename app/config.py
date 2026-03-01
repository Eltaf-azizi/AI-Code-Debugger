"""
Application Configuration
Enhanced configuration settings for AI Code Assistant
"""
import os
from functools import lru_cache
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # OpenAI Configuration
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
        self.TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.5"))
        self.MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
        
        # Application Configuration
        self.APP_NAME: str = os.getenv("APP_NAME", "AI Code Assistant")
        self.APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
        
        # File Handling
        self.MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "100000"))  # 100KB default
        self.CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "4000"))  # tokens per chunk
        self.MAX_CHUNKS: int = int(os.getenv("MAX_CHUNKS", "10"))
        
        # Database
        self.DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
        self.DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
        
        # Caching
        self.CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
        
        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = os.getenv(
            "LOG_FORMAT", 
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # API Configuration
        self.API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
        self.API_TITLE: str = os.getenv("API_TITLE", "AI Code Assistant API")
        self.API_DESCRIPTION: str = os.getenv(
            "API_DESCRIPTION", 
            "AI-powered code analysis, debugging, and optimization API"
        )
        
        # CORS
        self.CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
        
        # Rate Limiting
        self.RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
        self.RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
        
        # Security
        self.SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    @property
    def is_configured(self) -> bool:
        """Check if the application is properly configured."""
        return bool(self.OPENAI_API_KEY)
    
    def validate(self) -> list:
        """
        Validate configuration and return list of errors.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        if self.MAX_FILE_SIZE <= 0:
            errors.append("MAX_FILE_SIZE must be positive")
        
        if self.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE must be positive")
        
        if self.TEMPERATURE < 0 or self.TEMPERATURE > 1:
            errors.append("TEMPERATURE must be between 0 and 1")
        
        return errors


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()


# Export settings for easy import
settings = get_settings()
