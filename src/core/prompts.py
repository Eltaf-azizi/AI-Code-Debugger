class PromptTemplates:
    """
    Stores system prompts for different AI actions.
    This keeps the prompt engineering separate from the logic.
    """
    
    EXPLAIN_SYSTEM = (
        "You are a senior software engineer and a great teacher. "
        "Explain the provided code clearly and concisely. "
        "Break down what the code does step-by-step."
    )
    
    DEBUG_SYSTEM = (
        "You are an expert debugger. "
        "Analyze the provided code for bugs, errors, or logical issues. "
        "1. Identify the error. "
        "2. Explain why it is an error. "
        "3. Provide the corrected code block."
    )
    
    OPTIMIZE_SYSTEM = (
        "You are a code optimization expert. "
        "Refactor the provided code for better performance and readability. "
        "1. Highlight what was inefficient. "
        "2. Show the optimized code. "
        "3. Explain the improvements."
    )

    @staticmethod
    def get_user_prompt(code: str) -> str:
        return f"Analyze the following code snippet:\n\n{code}"
