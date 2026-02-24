"""
Advanced AI Code Debugger - Main Entry Point

A professional, feature-rich code analysis tool powered by AI.
Features:
- Smart debugging with error detection
- Security vulnerability analysis
- Performance optimization
- Code refactoring
- Test generation
- Documentation generation
- Code review
- Multi-file project analysis
- Session history
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))


def main():
    """Main entry point for the application."""
    from src.ui.layout import render_main_page
    
    # Run the Streamlit app
    render_main_page()


if __name__ == "__main__":
    main()
