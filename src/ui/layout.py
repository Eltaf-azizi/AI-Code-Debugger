"""
Advanced Layout for AI Code Debugger.
Main application layout with tabs and advanced features.
"""
import streamlit as st
from streamlit.runtime.scriptrunner import script_run_context
import time
from typing import Optional, Dict, List

from src.core.ai_engine import CodeAnalyzer, get_analyzer, reset_analyzer
from src.core.prompts import detect_language
from src.ui.components import (
    display_header,
    display_sidebar,
    display_action_buttons,
    display_code_editor,
    display_file_uploader,
    display_result,
    display_history,
    display_error_box,
    display_info_box,
    display_success_box,
    display_loading_spinner,
    display_metrics
)


# Page configuration
st.set_page_config(
    page_title="Advanced AI Code Debugger",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': '# Advanced AI Code Debugger\nIntelligent code analysis powered by AI',
        'Report a bug': None,
        'Get help': None
    }
)


# Session state initialization
def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'analyzer': None,
        'history': [],
        'current_code': '',
        'current_result': None,
        'current_action': None,
        'file_uploaded': False,
        'uploaded_file_content': None,
        'sidebar_config': {},
        'session_active': False,
        'analysis_count': 0,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_main_page():
    """Main function to render the advanced application layout."""
    
    # Initialize session state
    init_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar and get configuration
    sidebar_config = display_sidebar()
    st.session_state.sidebar_config = sidebar_config
    
    # Handle API key
    api_key = sidebar_config.get("api_key", "")
    
    # Configure analyzer if API key provided
    if api_key and (not st.session_state.analyzer or api_key != st.session_state.get('_api_key', '')):
        try:
            from src.utils.config import settings
            settings.OPENAI_API_KEY = api_key
            st.session_state._api_key = api_key
            reset_analyzer()
            st.session_state.analyzer = get_analyzer()
            display_success_box("API Key configured successfully!")
        except Exception as e:
            display_error_box(f"Failed to configure API: {e}")
    
    # Check if analyzer is initialized
    if not st.session_state.analyzer:
        try:
            st.session_state.analyzer = get_analyzer()
        except ValueError as e:
            display_warning_box(str(e))
    
    # Create main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Code Analysis",
        "📁 File Analysis", 
        "📜 History",
        "⚙️ Settings"
    ])
    
    with tab1:
        render_code_analysis_tab(sidebar_config)
    
    with tab2:
        render_file_analysis_tab(sidebar_config)
    
    with tab3:
        render_history_tab()
    
    with tab4:
        render_settings_tab()


def render_code_analysis_tab(sidebar_config: Dict):
    """Render the main code analysis tab."""
    
    # Create two columns: main editor and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Code")
        
        # Check for uploaded file content
        if st.session_state.get('uploaded_file_content'):
            code = display_code_editor(st.session_state.uploaded_file_content)
        else:
            code = display_code_editor()
        
        st.session_state.current_code = code
        
        # Action buttons
        action = display_action_buttons()
        st.session_state.current_action = action
        
        # Analyze button
        if action and code:
            if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
                analyze_code(code, action, sidebar_config)
        elif action and not code:
            display_warning_box("Please enter some code to analyze!")
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        # Display result if available
        if st.session_state.current_result:
            display_result(
                st.session_state.current_result,
                st.session_state.current_action
            )
            
            # Show metrics if available
            if st.session_state.get('analysis_metrics'):
                st.markdown("---")
                display_metrics(st.session_state.analysis_metrics)
        else:
            # Placeholder when no result
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.5);">
                <span style="font-size: 4rem;">💡</span>
                <p>Enter your code and select an action to get started</p>
            </div>
            """, unsafe_allow_html=True)


def render_file_analysis_tab(sidebar_config: Dict):
    """Render the file analysis tab."""
    
    st.markdown("### 📁 Upload and Analyze Files")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a code file",
            type=['py', 'js', 'ts', 'tsx', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 
                  'rb', 'php', 'swift', 'kt', 'sql', 'html', 'css', 'json', 'yaml'],
            help="Upload a code file for analysis"
        )
        
        if uploaded_file:
            try:
                content = uploaded_file.getvalue().decode("utf-8")
                
                # Detect language
                detected_lang = detect_language(content)
                
                st.markdown(f"**Detected Language:** `{detected_lang}`")
                st.markdown(f"**File Size:** {uploaded_file.size:,} bytes")
                
                # Store for analysis
                st.session_state.uploaded_file_content = content
                
                # Show preview
                st.markdown("### 📄 File Preview")
                st.code(content[:2000] + "..." if len(content) > 2000 else content, 
                       language=detected_lang)
                
            except Exception as e:
                display_error_box(f"Error reading file: {e}")
                return
        else:
            st.session_state.uploaded_file_content = None
    
    with col2:
        # Multiple file upload
        st.markdown("### 📂 Multi-File Project Analysis")
        
        uploaded_files = st.file_uploader(
            "Upload multiple files",
            type=['py', 'js', 'ts', 'java', 'cpp', 'go', 'rs', 'rb', 'php'],
            accept_multiple_files=True,
            help="Upload multiple files for project-wide analysis"
        )
        
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} files uploaded**")
            
            # Show file list
            for f in uploaded_files:
                st.markdown(f"- 📄 {f.name} ({f.size:,} bytes)")
            
            # Project analysis option
            if st.button("🔍 Analyze Entire Project", type="primary"):
                analyze_project(uploaded_files, sidebar_config)
    
    # Project structure visualization placeholder
    st.markdown("---")
    st.markdown("### 🏗️ Project Structure")
    
    with st.expander("View Project Structure", expanded=False):
        st.info("Project structure visualization would appear here after uploading multiple files")


def render_history_tab():
    """Render the history tab."""
    
    st.markdown("### 📜 Analysis History")
    
    # Get analyzer history
    if st.session_state.analyzer:
        history = st.session_state.analyzer.get_session_history()
    else:
        history = []
    
    if not history:
        display_info_box("No analysis history yet. Start analyzing code to build your history!")
        return
    
    # Display history in a more structured way
    for i, session in enumerate(reversed(history[-20:])):
        with st.expander(f"🕐 {session['action']} - {session['timestamp'][:19]}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Code:**")
                st.code(session['code'][:500] + "..." if len(session['code']) > 500 else session['code'])
            
            with col2:
                st.markdown("**Language:**")
                st.write(session['language'])
                
                if st.button(f"Load Result #{i+1}", key=f"load_{session['id']}"):
                    st.session_state.current_result = session['result']
                    st.session_state.current_action = session['action']
                    st.rerun()
    
    # Clear history button
    if st.button("🗑️ Clear History", type="secondary"):
        if st.session_state.analyzer:
            st.session_state.analyzer.clear_history()
        st.rerun()


def render_settings_tab():
    """Render the settings tab."""
    
    st.markdown("### ⚙️ Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔑 API Settings")
        
        # Model selection
        model = st.selectbox(
            "AI Model",
            ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0,
            help="Select the AI model"
        )
        
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Controls randomness in output"
        )
        
        # Max tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=500,
            max_value=16000,
            value=4000,
            step=500,
            help="Maximum tokens in response"
        )
        
    with col2:
        st.markdown("#### 🎨 UI Settings")
        
        # Theme (placeholder - Streamlit has limited theme support)
        theme = st.selectbox(
            "Theme",
            ["Dark (Default)", "Light", "System"],
            help="UI Theme (Dark mode recommended)"
        )
        
        # Show line numbers
        show_line_numbers = st.checkbox("Show line numbers in code", value=True)
        
        # Enable animations
        enable_animations = st.checkbox("Enable animations", value=True)
        
        # Auto-save sessions
        auto_save = st.checkbox("Auto-save sessions", value=True)
    
    st.markdown("---")
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📡 Connection")
            
            # Timeout
            timeout = st.number_input(
                "Request Timeout (seconds)",
                min_value=10,
                max_value=300,
                value=60
            )
            
            # Retry attempts
            retries = st.number_input(
                "Retry Attempts",
                min_value=0,
                max_value=5,
                value=3
            )
            
        with col2:
            st.markdown("#### 💾 Data Management")
            
            # Clear cache
            if st.button("Clear Cache"):
                st.cache_data.clear()
                display_success_box("Cache cleared!")
            
            # Export settings
            if st.button("Export Settings"):
                display_info_box("Settings export coming soon!")
            
            # Import settings
            if st.button("Import Settings"):
                display_info_box("Settings import coming soon!")
    
    # Save settings button
    st.markdown("---")
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        display_success_box("Settings saved successfully!")


def analyze_code(code: str, action: str, config: Dict):
    """Analyze code with the specified action.
    
    Args:
        code: The code to analyze
        action: The analysis action
        config: Configuration dictionary
    """
    if not st.session_state.analyzer:
        display_error_box("Analyzer not initialized. Please check your API key.")
        return
    
    language = config.get("language", "auto")
    if language == "auto":
        language = detect_language(code)
    
    try:
        with display_loading_spinner(f"Analyzing code ({action})..."):
            # Run the analysis
            result = st.session_state.analyzer.analyze(code)
            
            #, action, language Update session state
            st.session_state.current_result = result
            st.session_state.current_action = action
            st.session_state.analysis_count += 1
            
            # Set some basic metrics
            st.session_state.analysis_metrics = {
                "Lines": len(code.split('\n')),
                "Chars": len(code),
                "Language": language,
                "Action": action
            }
            
            st.rerun()
            
    except Exception as e:
        display_error_box(f"Analysis failed: {str(e)}")


def analyze_project(files: List, config: Dict):
    """Analyze multiple files as a project.
    
    Args:
        files: List of uploaded files
        config: Configuration dictionary
    """
    if not st.session_state.analyzer:
        display_error_box("Analyzer not initialized. Please check your API key.")
        return
    
    try:
        # Read all file contents
        file_contents = {}
        for f in files:
            content = f.getvalue().decode("utf-8")
            file_contents[f.name] = content
        
        with display_loading_spinner("Analyzing project..."):
            # For now, just analyze each file separately
            results = []
            for filename, content in file_contents.items():
                result = st.session_state.analyzer.analyze(
                    content, 
                    "Explain",  # Use explain for overview
                    detect_language(content)
                )
                results.append({
                    "file": filename,
                    "analysis": result
                })
            
            # Display project overview
            st.markdown("### 📊 Project Analysis Results")
            
            for res in results:
                with st.expander(f"📄 {res['file']}", expanded=False):
                    st.markdown(res['analysis'])
                    
    except Exception as e:
        display_error_box(f"Project analysis failed: {str(e)}")


# Entry point
if __name__ == "__main__":
    render_main_page()
