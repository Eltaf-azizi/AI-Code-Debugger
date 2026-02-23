import streamlit as st

def display_header():
    """Displays the main title and description."""
    st.title("🐛 AI Code Explainer & Debugger")
    st.markdown(
        """
        An intelligent tool to help you understand, debug, and optimize your code.
        **Paste your code on the left and choose an action.**
        """
    )
    st.divider()

def display_sidebar():
    """Displays the sidebar configuration."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", help="You can also set this in your .env file")
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "This app uses GPT-3.5 to analyze code. "
            "Your code is sent to OpenAI for processing."
        )
        st.markdown("### Actions Guide")
        st.markdown("- ✨ **Explain**: Understand code logic.")
        st.markdown("- 🐞 **Debug**: Find and fix errors.")
        st.markdown("- 🚀 **Optimize**: Improve performance.")
        
        return api_key
