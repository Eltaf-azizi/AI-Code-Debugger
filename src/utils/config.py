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
    MODEL_NAME: str = "gpt-3.5-turbo" # Default model
    
    # Validation
    @property
    def is_configured(self):
        return bool(self.OPENAI_API_KEY)

settings = Settings()
