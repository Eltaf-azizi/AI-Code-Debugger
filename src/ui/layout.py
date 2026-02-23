import streamlit as st
from src.core.ai_engine import CodeAnalyzer
from src.ui.components import display_header, display_sidebar

def render_main_page():
    """Main function to render the application layout."""
    
    # 1. Render UI Components
    display_header()
    api_key_input = display_sidebar()

    # 2. Code Input Area
    # Using columns to center the input slightly or manage layout
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        user_code = st.text_area(
            "Paste your code here:", 
            height=250, 
            placeholder="# Write your Python, JavaScript, or C++ code here..."
        )

        # 3. Action Buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            explain_btn = st.button("✨ Explain Code", use_container_width=True)
        with btn_col2:
            debug_btn = st.button("🐞 Find Bugs", use_container_width=True)
        with btn_col3:
            optimize_btn = st.button("🚀 Optimize", use_container_width=True)

    # 4. Handle Logic & API Calls
    action = None
    if explain_btn:
        action = "Explain"
    elif debug_btn:
        action = "Debug"
    elif optimize_btn:
        action = "Optimize"

    if action and user_code:
        # Check for API Key (Priority: Input > .env)
        if api_key_input:
            # Temporarily override settings if user provided key in UI
            from src.utils.config import settings
            settings.OPENAI_API_KEY = api_key_input
            
        try:
            analyzer = CodeAnalyzer()
            
            with st.spinner(f"Analyzing code ({action})... 🧠"):
                result = analyzer.analyze(user_code, action)
                
                st.divider()
                st.markdown(f"### 📝 Result: **{action}**")
                st.markdown(result)
                
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            
    elif action and not user_code:
        st.warning("Please paste some code first!")

if __name__ == "__main__":
    render_main_page()
