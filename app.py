# app.py 

import streamlit as st
import requests
from audiorecorder import audiorecorder
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Assessli-Verse | AI Interviewer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Polished Look & Splash Screen ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    
    .main-title {
        font-size: 3.25rem;
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
    }
    
    h2 { /* Subheaders like "Interview for..." */
        color: #E0E0E0;
        border-bottom: 1px solid #444;
        padding-bottom: 10px;
        text-align: center;
    }
    .block-container {
        max-width: 900px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    /* --- The Splash Screen Styling --- */
    .splash-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        position: relative;
        text-align: center;
    }
    .splash-text {
        font-size: 4.5rem;
        font-weight: bold;
        color: #FFFFFF;
        line-height: 1.2;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# --- Application Header ---
st.markdown("<p class='main-title'>🎙️ Assessli-Verse: The AI Voice Interviewer</p>", unsafe_allow_html=True)


# --- API URL ---
API_URL = "http://127.0.0.1:8000"

# --- Session State Initialization ---
if "status" not in st.session_state:
    st.session_state.status = "not_started"
if "conversation_log" not in st.session_state:
    st.session_state.conversation_log = []
if "role" not in st.session_state:
    st.session_state.role = "Junior Python Developer"
if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = None
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# --- UI Rendering Logic ---

# STATE 1: Initial Screen
if st.session_state.status == "not_started":
    st.header("📋 Select a Role to Begin")
    col1, col2 = st.columns([3, 1])
    with col1:
        role_options = ["Junior Python Developer", "Product Manager", "Data Analyst", "UX/UI Designer"]
        st.session_state.role = st.selectbox("I'm interviewing for the role of:", role_options, label_visibility="collapsed")
    
    with col2:
        if st.button("Start Voice Interview", use_container_width=True, type="primary"):
            st.session_state.status = "show_splash"
            st.rerun()

# STATE 2: The High-Impact Splash Screen
elif st.session_state.status == "show_splash":
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.balloons() # Left balloons
    with col2:
        st.markdown("""
            <div class='splash-container'>
                <div>
                    <p class='splash-text'>ALL THE BEST</p>
                    <p class='splash-text'>&</p>
                    <p class='splash-text'>BE CONFIDENT</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.balloons() # Right balloons
    time.sleep(3.5)
    st.session_state.status = "connecting"
    st.rerun()

# STATE 3: Connecting
elif st.session_state.status == "connecting":
    with st.spinner("Connecting to the interview agent..."):
        try:
            url = f"{API_URL}/start-interview/{st.session_state.role}"
            response = requests.post(url)
            response.raise_for_status()
            st.session_state.conversation_id = response.headers.get("X-Conversation-Id")
            st.session_state.conversation_log = [{"type": "ai", "data": response.content}]
            st.session_state.status = "in_progress"
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Connection failed: {e}. Please ensure the backend server is running.")
            st.session_state.status = "not_started"

# STATE 4 & 5: Interview in Progress & Awaiting Processing
elif st.session_state.status in ["in_progress", "awaiting_processing"]:
    st.header(f"Interview for: {st.session_state.role}")
    
    for msg in st.session_state.conversation_log:
        if msg["type"] == "ai":
            with st.chat_message("assistant", avatar="🤖"):
                st.audio(msg["data"], format='audio/mpeg')
        elif msg["type"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.success("Your answer has been sent.")
    
    if st.session_state.status == "in_progress":
        with st.container(border=True):
            st.subheader("Your Answer")
            audio = audiorecorder("Record Your Answer Now", "Stop Recording")
            if len(audio) > 0:
                st.session_state.recorded_audio = audio.export().read()
                st.session_state.status = "awaiting_processing"
                st.rerun()

    if st.session_state.status == "awaiting_processing":
        with st.container(border=True):
            st.subheader("Your Recorded Answer")
            st.audio(st.session_state.recorded_audio, format="audio/mp3")
            if st.button("Process My Answer", use_container_width=True, type="primary"):
                st.session_state.status = "processing"
                st.rerun()

# STATE 6: Processing
elif st.session_state.status == "processing":
    with st.spinner("Analyzing your answer..."):
        try:
            url = f"{API_URL}/process-answer/{st.session_state.conversation_id}"
            files = {'audio_file': ('answer.mp3', st.session_state.recorded_audio, 'audio/mpeg')}
            response = requests.post(url, files=files)
            response.raise_for_status()
            st.session_state.recorded_audio = None
            st.session_state.conversation_log.append({"type": "user", "data": "sent"})
            
            content_type = response.headers.get("Content-Type")
            if "text/plain" in content_type:
                st.session_state.status = "finished"
                st.session_state.conversation_log.append({"type": "report", "data": response.text})
            else:
                st.session_state.status = "in_progress"
                st.session_state.conversation_log.append({"type": "ai", "data": response.content})
            
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to process answer: {e}")
            st.session_state.status = "in_progress"
            st.rerun()

# STATE 7: Interview Finished
elif st.session_state.status == "finished":
    st.header("🏆 Your Interview Performance Report")
    report_msg = next((msg for msg in st.session_state.conversation_log if msg["type"] == "report"), None)
    if report_msg:
        st.markdown(report_msg["data"], unsafe_allow_html=True)
    if st.button("Start a New Interview", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()