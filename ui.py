#!/usr/bin/env python3
"""
OmniCoach Frontend Dashboard - Stable Hackathon Edition
High-velocity Streamlit UI with robust mock/live pipeline switching toggles.
"""

import streamlit as st
import requests

# App Page Layout Design Configuration
st.set_page_config(
    page_title="OmniCoach Panel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling injection for clean hackathon look
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    h1 { color: #00ffcc; font-weight: 800; }
    h2, h3 { color: #ffffff; }
    .stButton>button { background-color: #00ffcc; color: #0e1117; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniCoach: AI Biomechanical Suite")
st.subheader("High-velocity multi-agent performance tracking & pro-level benchmarking")
st.write("---")

# ── SIDEBAR SELECTION LAYER ──
st.sidebar.header("📋 Session Parameters")
sport_choice = st.sidebar.selectbox(
    "Target Discipline:",
    ["Football", "Basketball", "Tennis", "Cricket", "Athletics"]
)

# Live Demonstration vs Sandbox Mock Toggle
demo_mode = st.sidebar.checkbox("Use Demo / Sandbox Mode", value=False, help="Enable this to test using integrated mock video payloads without transferring massive files over Wi-Fi.")

uploaded_file = None
if not demo_mode:
    uploaded_file = st.sidebar.file_uploader(
        "Upload Training Clip (MP4/MOV):",
        type=["mp4", "mov", "avi"]
    )
else:
    st.sidebar.success("Sandbox Mode Active: System will pipeline deterministic tracking configurations.")

st.sidebar.write("---")
st.sidebar.info("🤖 Powered by Google Antigravity Multi-Agent Framework & MediaPipe 3D Kinematics.")

# ── MAIN PANEL INTERACTION LAYER ──
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎞️ Input Vector Source")
    if demo_mode:
        st.info(f"Using mock vector asset: `mock://training_session_2026-07-04.mp4` ({sport_choice})")
        st.write("The multi-agent pipeline will evaluate pre-loaded skeleton telemetry strings to mimic video inferences.")
    elif uploaded_file is not None:
        st.video(uploaded_file)
        st.success(f"Stream loaded cleanly: {uploaded_file.name}")
    else:
        st.warning("Awaiting video ingestion or sandbox deployment toggle selection.")

with col2:
    st.header("📊 Generated Coaching CV")
    
    # Validation constraint check to confirm we have an active payload pipeline
    if demo_mode or (uploaded_file is not None):
        if st.sidebar.button("Run Multi-Agent Analysis Pipeline"):
            with st.spinner(f"Processing 3D coordinate frames & calling multi-agent matrix..."):
                try:
                    backend_url = "http://localhost:8000/api/v1/analyze"
                    
                    if demo_mode:
                        # Construct a mock multipart profile stream to keep the schema happy
                        files = {"video": ("mock_session.mp4", b"fake_bytes", "video/mp4")}
                        data = {"sport": sport_choice.lower()}
                    else:
                        files = {"video": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        data = {"sport": sport_choice.lower()}
                    
                    response = requests.post(backend_url, files=files, data=data)
                    
                    if response.status_code == 200:
                        payload = response.json()
                        st.balloons()
                        st.markdown(payload["coaching_cv"])
                    else:
                        st.error(f"Backend Server Error ({response.status_code}): {response.text}")
                        
                except Exception as e:
                    st.error(f"Failed to communicate with API service layer: {str(e)}")
    else:
        st.info("Upload a localized training session recording to trigger pipeline execution models.")
