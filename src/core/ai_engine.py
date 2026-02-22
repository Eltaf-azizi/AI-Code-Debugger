from openai import OpenAI
from src.utils.config import settings
from src.core.prompts import PromptTemplates

class CodeAnalyzer:
    """
    Handles communication with the OpenAI API.
    """
    
    def __init__(self):
        if not settings.is_configured:
            raise ValueError("OpenAI API Key is missing. Please check your .env file.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def analyze(self, code: str, action: str) -> str:
        """
        Sends code to the AI model for analysis based on the action type.
        """
        # Select the appropriate system prompt
        if action == "Explain":
            system_msg = PromptTemplates.EXPLAIN_SYSTEM
        elif action == "Debug":
            system_msg = PromptTemplates.DEBUG_SYSTEM
        elif action == "Optimize":
            system_msg = PromptTemplates.OPTIMIZE_SYSTEM
        else:
            return "Error: Invalid action specified."

        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": PromptTemplates.get_user_prompt(code)}
                ],
                temperature=0.5, # Balanced creativity
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"An API error occurred: {str(e)}"
