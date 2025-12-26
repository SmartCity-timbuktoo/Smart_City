"""
Addis-Sync Streamlit UI (Session-Enabled Version)
Web interface for the Addis-Sync multi-agent urban services platform with ADK session management.
# Triggering reload for debug capture 2
"""

import streamlit as st
import os
import uuid
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- ADK Component Loading ---
# --- ADK Component Loading ---
try:
    from smart_city_agent.local_runner import AdkApp
    from smart_city_agent.agent import customer_service_agent
    from smart_city_agent.session_manager import get_session_service
    from smart_city_agent.message_processor import process_message_with_agent
    ADK_AVAILABLE = True
except ImportError as e:
    ADK_AVAILABLE = False
    IMPORT_ERROR = str(e)
    # Log critical failure
    try:
        with open("status_log.txt", "w") as f:
             f.write(f"STATUS: CRITICAL_IMPORT_ERROR\nError: {str(e)}\nTraceback:\n{traceback.format_exc()}")
    except:
        pass

# Page configuration
st.set_page_config(
    page_title="Addis-Sync - Urban Services",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Google Material Theme */
    .stApp { background-color: #FFFFFF; font-family: 'Roboto', sans-serif; }
    
    /* Header */
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1A73E8; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1rem; color: #5F6368; margin-bottom: 2rem; }
    
    /* Sidebar Services */
    .service-card {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        font-weight: 500;
        display: flex;
        align-items: center;
        transition: transform 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .service-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.15); }
    
    .emergency { background-color: #FCE8E6; color: #C5221F; border-left: 5px solid #D93025; }
    .power { background-color: #FEF7E0; color: #B06000; border-left: 5px solid #F9AB00; }
    .sanitation { background-color: #E6F4EA; color: #137333; border-left: 5px solid #1E8E3E; }
    .infrastructure { background-color: #E8F0FE; color: #1967D2; border-left: 5px solid #1A73E8; }
    .utility { background-color: #E1F5FE; color: #0277BD; border-left: 5px solid #0288D1; }
    
    /* Chat Bubbles */
    .stChatMessage { padding: 1rem; border-radius: 12px; }
    
    /* Right Sidebar styling */
    .right-sidebar-header { font-size: 1.1rem; font-weight: 600; color: #202124; margin-top: 1rem; }
    .stat-card { background: #F8F9FA; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = bool(os.getenv('GOOGLE_API_KEY'))
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize ADK AdkApp (simplified initialization)
if 'adk_app' not in st.session_state:
    if ADK_AVAILABLE and st.session_state.api_key_valid:
        try:
            # Simplified initialization - AdkApp handles session management internally
            # when using Gemini API Key (GOOGLE_GENAI_USE_VERTEXAI=False)
            st.session_state.adk_app = AdkApp(agent=customer_service_agent)
            st.session_state.adk_status = "✅ AdkApp Active"
            # Log success
            with open("status_log.txt", "w") as f:
                f.write("STATUS: SUCCESS\nAdkApp initialized")
            print("✅ DEBUG: AdkApp successfully initialized")
        except Exception as e:
            st.session_state.adk_app = None
            st.session_state.adk_status = f"❌ Error: {str(e)}"
            # Log error
            with open("status_log.txt", "w") as f:
                f.write(f"STATUS: INIT_ERROR\nError: {str(e)}\nTraceback:\n{traceback.format_exc()}")
            print(f"❌ DEBUG: AdkApp failed to start: {e}")
    else:
        st.session_state.adk_app = None
        if not ADK_AVAILABLE:
            st.session_state.adk_status = f"❌ ADK Missing: {IMPORT_ERROR}"
            with open("status_log.txt", "w") as f:
                f.write(f"STATUS: IMPORT_ERROR\nError: {IMPORT_ERROR}")
        else:
            st.session_state.adk_status = "❌ API Key Missing"
            with open("status_log.txt", "w") as f:
                f.write("STATUS: KEY_ERROR\nAPI Key missing")

# Header
st.markdown('<div class="main-header">🏙️ Addis-Sync</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Urban Infrastructure Coordination Platform</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 System Status")
    
    # Display ADK status (shows detailed error if any)
    if 'adk_status' in st.session_state:
        if "✅" in st.session_state.adk_status:
            st.success(st.session_state.adk_status)
        elif "❌" in st.session_state.adk_status:
            st.error(st.session_state.adk_status)
        else:
            st.info(st.session_state.adk_status)
    elif not ADK_AVAILABLE:
        st.error(f"❌ ADK Missing: {IMPORT_ERROR}")
        st.info("Try: uv pip install google-adk vertexai")
    elif not st.session_state.api_key_valid:
        st.error("❌ API Key Missing")
        st.info("Add GOOGLE_API_KEY to .env file")
    else:
        st.warning("⚠️ Initializing...")
    
    st.markdown("---")
    st.header("🏢 Services")
    
    st.markdown('<div class="service-card emergency"><span>🚨 Emergency & Safety</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="service-card power"><span>⚡ Power & Electricity</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="service-card sanitation"><span>🗑️ Sanitation & Waste</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="service-card infrastructure"><span>🏗️ Infrastructure</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="service-card utility"><span>💧 Water & Utilities</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    # Status indicator compact
    if 'adk_status' in st.session_state and "✅" in st.session_state.adk_status:
         st.caption("🟢 System Online")
    else:
         st.caption("🔴 System Offline")

# Main content area
col1, col2 = st.columns([2, 1])

# Main content area - 3 Column Layout Implementation
# Ratio: [Chat Area (3)] | [Right Sidebar (1.2)]
col1, col2 = st.columns([3, 1.2])

with col1:
    st.header("💬 Addis-Sync Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input (Fixed Bottom by default in Streamlit)
    if prompt := st.chat_input("Describe your issue (e.g., 'No power in Bole')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing with agents..."):
                if st.session_state.adk_app:
                    try:
                        response = process_message_with_agent(
                            runner=st.session_state.adk_app,
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            prompt=prompt
                        )
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Agent Error: {str(e)}")
                else:
                    response = "⚠️ System not initialized. Check sidebar logs."
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # Right Sidebar Content
    st.markdown('<div class="right-sidebar-header">🛠️ Quick Actions</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.markdown('<div class="right-sidebar-header">💡 Try Asking</div>', unsafe_allow_html=True)
    
    # Sample Queries as pills/buttons
    queries = [
        "Report Pothole",
        "Power Outage",
        "No Water",
        "Garbage Pickup"
    ]
    
    for q in queries:
        if st.button(q, key=f"btn_{q}", use_container_width=True):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": q})
            
            # Process immediately
            if st.session_state.adk_app:
                try:
                    with st.spinner("Processing..."):
                        response = process_message_with_agent(
                            runner=st.session_state.adk_app,
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            prompt=q
                        )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
            
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="right-sidebar-header">📊 Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 1.5rem; font-weight: bold; color: #1A73E8;">{len(st.session_state.messages)}</div>
        <div style="font-size: 0.8rem; color: #666;">Messages</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Session ID: {st.session_state.session_id[:8]}")

st.markdown("---")
st.caption("Addis-Sync © 2025 | Addis Ababa Urban Services Coordination Platform")