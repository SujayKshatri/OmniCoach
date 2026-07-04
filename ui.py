#!/usr/bin/env python3
"""
OmniCoach Frontend Dashboard
High-velocity Streamlit UI for video ingestion and interactive coaching visualization.
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
# Custom styling injection for clean hackathon look
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    h1 { color: #00ffcc; font-weight: 800; }
    h2, h3 { color: #ffffff; }
    .stButton>button { background-color: #00ffcc; color: #0e1117; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)  # Swapped to unsafe_allow_html
st.title("⚡ OmniCoach: AI Biomechanical Suite")
st.subheader("High-velocity multi-agent performance tracking & pro-level benchmarking")
st.write("---")

# ── SIDEBAR SELECTION LAYER ──
st.sidebar.header("📋 Session Parameters")
sport_choice = st.sidebar.selectbox(
    "Target Discipline:",
    ["Football", "Basketball", "Tennis", "Cricket", "Athletics"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Training Clip (MP4/MOV):",
    type=["mp4", "mov", "avi"]
)

st.sidebar.write("---")
st.sidebar.info("🤖 Powered by Google Antigravity Multi-Agent Framework & MediaPipe 3D Kinematics.")

# ── MAIN PANEL INTERACTION LAYER ──
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎞️ Input Vector Source")
    if uploaded_file is not None:
        # Display the video immediately on the screen for the judges
        st.video(uploaded_file)
        st.success(f"Stream loaded cleanly: {uploaded_file.name}")
    else:
        st.warning("Awaiting video ingestion from the sidebar configuration panel.")

with col2:
    st.header("📊 Generated Coaching CV")
    
    if uploaded_file is not None:
        if st.sidebar.button("Run Multi-Agent Analysis Pipeline"):
            with st.spinner(f"Processing 3D coordinate frames & calling multi-agent matrix..."):
                try:
                    # Prepare multipart form data payload for FastAPI
                    files = {"video": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"sport": sport_choice.lower()}
                    
                    # Target endpoint matching our main.py architecture
                    backend_url = "http://localhost:8000/api/v1/analyze"
                    response = requests.post(backend_url, files=files, data=data)
                    
                    if response.status_code == 200:
                        payload = response.json()
                        st.balloons()
                        
                        # Render the complete Markdown report returned from the agents
                        st.markdown(payload["coaching_cv"])
                    else:
                        st.error(f"Backend Server Error ({response.status_code}): {response.text}")
                        
                except Exception as e:
                    st.error(f"Failed to communicate with API service layer: {str(e)}")
    else:
        st.info("Upload a localized training session recording to trigger pipeline execution models.")
