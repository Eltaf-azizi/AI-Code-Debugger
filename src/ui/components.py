"""
Enhanced UI Components for Advanced AI Code Debugger.
Modern, professional components with rich functionality.
"""
import streamlit as st
from streamlit.elements import button_pills
import hashlib
from datetime import datetime
from typing import List, Dict, Optional


# ============== CUSTOM CSS STYLES ==============

def get_custom_css() -> str:
    """Get custom CSS for modern styling."""
    return """
    <style>
    /* Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    /* Custom Title */
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00d4ff, #7c3aed, #00d4ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        padding: 1rem 0 !important;
        margin-bottom: 1rem !important;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(124, 58, 237, 0.5)); }
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Action Buttons */
    .action-btn {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%) !important;
        border: none !important;
        border-radius: 12px !important;
       .75rem  padding: 01.5rem !important;
        font-weight: 600 !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%) !important;
        border-color: #7c3aed !important;
    }
    
    /* Code Block Styling */
    .code-block {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        overflow-x: auto;
    }
    
    /* Status Indicators */
    .status-critical { color: #ff4757 !important; }
    .status-high { color: #ffa502 !important; }
    .status-medium { color: #ffdd59 !important; }
    .status-low { color: #2ed573 !important; }
    
    /* History Item */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid #7c3aed;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        background: rgba(255, 255, 255, 0.08);
        border-left-color: #00d4ff;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.3) 0%, rgba(124, 58, 237, 0.3) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Animated gradient background for header */
    .header-gradient {
        background: linear-gradient(-45deg, #0f0f23, #1a1a2e, #16213e, #1e3a8a);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Info Boxes */
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: rgba(255, 165, 2, 0.1);
        border-left: 4px solid #ffa502;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    
    .error-box {
        background: rgba(255, 71, 87, 0.1);
        border-left: 4px solid #ff4757;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: rgba(46, 213, 115, 0.1);
        border-left: 4px solid #2ed573;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    
    /* Divider */
    .custom-divider {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
    }
    
    /* Session Info */
    .session-info {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
    }
    </style>
    """


def display_header():
    """Display the main application header with title and description."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Title with gradient effect
    st.markdown("""
    <div class="header-gradient" style="padding: 1.5rem; border-radius: 16px; margin-bottom: 1rem;">
        <h1 class="main-title">🔍 Advanced AI Code Debugger</h1>
        <p style="text-align: center; color: rgba(255,255,255,0.7); font-size: 1.1rem;">
            Intelligent code analysis, debugging, and optimization powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <span style="font-size: 2rem;">🐛</span><br>
            <strong>Smart Debugging</strong>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <span style="font-size: 2rem;">🛡️</span><br>
            <strong>Security Analysis</strong>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <span style="font-size: 2rem;">⚡</span><br>
            <strong>Performance</strong>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <span style="font-size: 2rem;">📝</span><br>
            <strong>Auto-Documentation</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


def display_sidebar() -> Dict:
    """Display the sidebar with configuration and tools.
    
    Returns:
        Dictionary with sidebar inputs
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <span style="font-size: 3rem;">⚙️</span>
            <h2 style="color: white; margin-top: 0.5rem;">Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # API Configuration
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key or set it in .env file"
        )
        
        # Model Selection
        model = st.selectbox(
            "AI Model",
            ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            help="Select the AI model to use"
        )
        
        st.markdown("---")
        
        # Analysis Options
        st.markdown("### 🔧 Analysis Options")
        
        language = st.selectbox(
            "Programming Language",
            ["auto", "python", "javascript", "typescript", "java", "cpp", "csharp", 
             "go", "rust", "ruby", "php", "swift", "kotlin", "sql", "html", "css"],
            help="Select the programming language or use auto-detect"
        )
        
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Higher values make output more creative but less focused"
        )
        
        st.markdown("---")
        
        # Tools Section
        st.markdown("### 🛠️ Tools")
        
        enable_history = st.checkbox("Session History", value=True, help="Track analysis history")
        enable_file_upload = st.checkbox("File Upload", value=True, help="Allow uploading code files")
        enable_comparison = st.checkbox("Code Comparison", value=True, help="Compare code versions")
        
        st.markdown("---")
        
        # About Section
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            **Advanced AI Code Debugger** uses GPT models to analyze, debug, optimize, and document your code.
            
            **Features:**
            - 🐛 Bug detection and fixes
            - 🔒 Security vulnerability analysis
            - ⚡ Performance optimization
            - 📝 Auto-documentation
            - 🧪 Test generation
            - 🔄 Code refactoring
            
            Your code is sent to OpenAI for processing. No code is stored.
            """)
        
        # Keyboard Shortcuts
        with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
            st.markdown("""
            - `Ctrl+Enter`: Run analysis
            - `Ctrl+S`: Save session
            - `Ctrl+L`: Clear code
            """)
        
        return {
            "api_key": api_key,
            "model": model,
            "language": language,
            "temperature": temperature,
            "enable_history": enable_history,
            "enable_file_upload": enable_file_upload,
            "enable_comparison": enable_comparison
        }


def display_action_buttons() -> str:
    """Display action buttons for different analysis types.
    
    Returns:
        Selected action name
    """
    st.markdown("### 🎯 Choose Action")
    
    # Main action buttons in a grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        explain_btn = st.button(
            "✨ Explain",
            use_container_width=True,
            help="Understand what the code does"
        )
    with col2:
        debug_btn = st.button(
            "🐛 Debug",
            use_container_width=True,
            help="Find and fix bugs"
        )
    with col3:
        optimize_btn = st.button(
            "🚀 Optimize",
            use_container_width=True,
            help="Improve performance"
        )
    with col4:
        security_btn = st.button(
            "🛡️ Security",
            use_container_width=True,
            help="Check for vulnerabilities"
        )
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        refactor_btn = st.button(
            "🔄 Refactor",
            use_container_width=True,
            help="Improve code structure"
        )
    with col6:
        test_btn = st.button(
            "🧪 Test",
            use_container_width=True,
            help="Generate unit tests"
        )
    with col7:
        docs_btn = st.button(
            "📝 Docs",
            use_container_width=True,
            help="Generate documentation"
        )
    with col8:
        review_btn = st.button(
            "👀 Review",
            use_container_width=True,
            help="Comprehensive code review"
        )
    
    # Determine which action was selected
    if explain_btn:
        return "Explain"
    elif debug_btn:
        return "Debug"
    elif optimize_btn:
        return "Optimize"
    elif security_btn:
        return "Security"
    elif refactor_btn:
        return "Refactor"
    elif test_btn:
        return "Generate Tests"
    elif docs_btn:
        return "Document"
    elif review_btn:
        return "Review"
    return None


def display_code_editor(default_code: str = "") -> str:
    """Display a code editor area with syntax highlighting options.
    
    Args:
        default_code: Default code to display in editor
        
    Returns:
        User-entered code
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code = st.text_area(
            "📝 Code Editor",
            value=default_code,
            height=350,
            placeholder="Paste your code here or upload a file...\n\nSupported languages: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, SQL, HTML, CSS",
            help="Enter the code you want to analyze"
        )
    
    with col2:
        st.markdown("### 📋 Quick Actions")
        
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
        format_btn = st.button("✨ Format", use_container_width=True)
        copy_btn = st.button("📋 Copy", use_container_width=True)
        
        if "code_buffer" not in st.session_state:
            st.session_state.code_buffer = ""
            
        if clear_btn:
            st.session_state.code_buffer = ""
            st.rerun()
            
        if format_btn and code:
            st.info("Code formatting would be applied here")
            
        if copy_btn and code:
            st.toast("Code copied to clipboard!")
    
    return code


def display_file_uploader() -> Optional[Dict]:
    """Display file upload component.
    
    Returns:
        Dictionary with uploaded file info or None
    """
    st.markdown("### 📁 Upload Code Files")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['py', 'js', 'ts', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'rb', 'php', 'swift', 'kt', 'sql', 'html', 'css', 'json', 'yaml', 'yml', 'txt'],
        help="Upload a code file for analysis"
    )
    
    if uploaded_file is not None:
        # Read file content
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            return {
                "name": uploaded_file.name,
                "content": content,
                "size": uploaded_file.size,
                "type": uploaded_file.type
            }
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    
    return None


def display_result(result: str, action: str):
    """Display analysis result with formatting.
    
    Args:
        result: The analysis result text
        action: The action that was performed
    """
    # Result header
    icons = {
        "Explain": "✨",
        "Debug": "🐛",
        "Optimize": "🚀",
        "Security": "🛡️",
        "Refactor": "🔄",
        "Generate Tests": "🧪",
        "Document": "📝",
        "Review": "👀"
    }
    
    icon = icons.get(action, "📋")
    
    st.markdown(f"""
    <div class="card">
        <h2 style="margin: 0; color: white;">{icon} {action} Result</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the result
    st.markdown(result)
    
    # Add action buttons for the result
    col1, col2, col3 = st.columns(3)
    
    with col1:
        copy_result_btn = st.button("📋 Copy Result", use_container_width=True)
    
    with col2:
        download_btn = st.button("💾 Download", use_container_width=True)
    
    with col3:
        share_btn = st.button("🔗 Share", use_container_width=True)
    
    if copy_result_btn:
        st.toast("Result copied to clipboard!")
    
    if download_btn:
        # Would implement file download
        st.info("Download feature coming soon!")


def display_history(history: List[Dict]):
    """Display session history.
    
    Args:
        history: List of session history items
    """
    st.markdown("### 📜 Session History")
    
    if not history:
        st.info("No analysis history yet. Run some analyses to see them here!")
        return
    
    for item in reversed(history[-10:]):  # Show last 10
        timestamp = datetime.fromisoformat(item['timestamp']).strftime("%H:%M:%S")
        
        st.markdown(f"""
        <div class="history-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #00d4ff;">{item['action']}</strong>
                    <span style="color: rgba(255,255,255,0.5);"> • {item['language']}</span>
                </div>
                <div class="session-info">{timestamp}</div>
            </div>
            <div class="session-info" style="margin-top: 0.5rem;">
                {item['code'][:50]}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add view button
        if st.button(f"View {item['id']}", key=f"view_{item['id']}"):
            st.session_state.selected_session = item


def display_comparison(original: str, modified: str):
    """Display code comparison view.
    
    Args:
        original: Original code
        modified: Modified code
    """
    st.markdown("### 🔄 Code Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Code**")
        st.code(original, language="python")
        
    with col2:
        st.markdown("**Modified Code**")
        st.code(modified, language="python")


def display_error_box(message: str):
    """Display an error message box.
    
    Args:
        message: Error message to display
    """
    st.markdown(f"""
    <div class="error-box">
        <strong>❌ Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def display_warning_box(message: str):
    """Display a warning message box.
    
    Args:
        message: Warning message to display
    """
    st.markdown(f"""
    <div class="warning-box">
        <strong>⚠️ Warning:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def display_info_box(message: str):
    """Display an info message box.
    
    Args:
        message: Info message to display
    """
    st.markdown(f"""
    <div class="info-box">
        <strong>ℹ️ Info:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def display_success_box(message: str):
    """Display a success message box.
    
    Args:
        message: Success message to display
    """
    st.markdown(f"""
    <div class="success-box">
        <strong>✅ Success:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def display_loading_spinner(message: str = "Analyzing..."):
    """Display a loading spinner with custom message.
    
    Args:
        message: Message to display during loading
    """
    return st.spinner(f"🔄 {message}...")


def display_metrics(metrics: Dict):
    """Display analysis metrics.
    
    Args:
        metrics: Dictionary of metrics to display
    """
    cols = st.columns(len(metrics))
    
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(label=key, value=value)
