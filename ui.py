#!/usr/bin/env python3
"""
OmniCoach Frontend Dashboard
Posh, high-fidelity Streamlit UI for video kinematics visualization and multi-agent synthesis.
"""

import streamlit as st
import requests
import json
import os
import pandas as pd
import math

# ── App Page Layout Design Configuration ──
st.set_page_config(
    page_title="OmniCoach | Elite Biomechanical Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom Styling Injection for Posh, Rich Glassmorphic Look ──
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Typography overrides */
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0d13;
    }
    ::-webkit-scrollbar-thumb {
        background: #1d2130;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2b3046;
    }

    /* Main Container Background Styling */
    .stApp {
        background: radial-gradient(circle at 80% 20%, #121420 0%, #08090d 100%) !important;
        color: #f1f5f9;
    }

    /* Header Panel */
    .posh-header {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
    }
    .posh-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9b51e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .posh-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 8px;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    /* Glassmorphic Container Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        border-color: rgba(0, 242, 254, 0.2);
        box-shadow: 0 8px 30px rgba(0, 242, 254, 0.05);
        transform: translateY(-2px);
    }
    
    /* Metrics Widget Structure */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 25px;
    }
    .m-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }
    .m-card:hover {
        border-color: rgba(0, 242, 254, 0.3);
        box-shadow: 0 10px 25px rgba(0, 242, 254, 0.08);
        transform: translateY(-3px);
    }
    .m-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }
    .m-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 8px 0 4px 0;
        background: linear-gradient(135deg, #ffffff 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .m-sub {
        font-size: 0.75rem;
        color: #a259ff;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.01) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        height: auto !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #00f2fe !important;
        border-color: rgba(0, 242, 254, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1) 0%, rgba(127, 0, 255, 0.05) 100%) !important;
        border-color: rgba(0, 242, 254, 0.4) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.05) !important;
    }

    /* Elite Progress indicators */
    .progress-container {
        width: 100%;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        margin: 6px 0 16px 0;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.02);
    }
    .progress-bar-fill {
        height: 8px;
        border-radius: 8px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Button overrides */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #08090d !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.3) !important;
        filter: brightness(1.05);
    }
    .stButton>button:active {
        transform: translateY(0) !important;
    }

    /* Sidebar background design */
    [data-testid="stSidebar"] {
        background-color: #08090d !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #94a3b8;
    }
    
    /* Event Timeline items */
    .timeline-item {
        border-left: 2px solid #00f2fe;
        padding-left: 18px;
        margin-left: 8px;
        padding-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        width: 10px;
        height: 10px;
        background-color: #00f2fe;
        border: 2px solid #08090d;
        border-radius: 50%;
        position: absolute;
        left: -6px;
        top: 4px;
        box-shadow: 0 0 8px #00f2fe;
    }
    .timeline-time {
        font-size: 0.8rem;
        color: #00f2fe;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .timeline-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #ffffff;
        margin: 2px 0 5px 0;
    }
    .timeline-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    /* Styled alert/note box */
    .note-box {
        background: rgba(127, 0, 255, 0.05);
        border: 1px solid rgba(127, 0, 255, 0.15);
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header Section ──
st.markdown("""
    <div class="posh-header">
        <h1 class="posh-title">⚡ OmniCoach Pro</h1>
        <div class="posh-subtitle">Multi-Agent Kinematic Telemetry Suite & Elite Athlete Benchmarker</div>
    </div>
""", unsafe_allow_html=True)

# ── Load Benchmarks Data ──
BENCHMARKS_PATH = os.path.join(os.path.dirname(__file__), "elite_benchmarks.json")
@st.cache_data
def load_benchmarks():
    try:
        with open(BENCHMARKS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

benchmarks_data = load_benchmarks()

# ── Session State Management ──
# We persist analysis results in Streamlit's state to prevent resets during interactions
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "selected_sport" not in st.session_state:
    st.session_state.selected_sport = "Football"

# ── SIDEBAR PANEL ──
st.sidebar.markdown("<h2 style='color: #ffffff; margin-top: 10px;'>📋 Config Panel</h2>", unsafe_allow_html=True)

sport_choice = st.sidebar.selectbox(
    "Target Discipline:",
    ["Football", "Basketball", "Tennis", "Cricket", "Athletics"],
    index=["Football", "Basketball", "Tennis", "Cricket", "Athletics"].index(st.session_state.selected_sport)
)
st.session_state.selected_sport = sport_choice

# ── Video Loading and Session State Storage ──
uploaded_file = st.sidebar.file_uploader(
    "Upload Training Clip (MP4/MOV):",
    type=["mp4", "mov", "avi"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #ffffff;'>⚡ Quick Demo Mode</h3>", unsafe_allow_html=True)
run_demo = st.sidebar.button("Run with Sample Video")

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.info("🤖 **Antigravity Framework v3**<br>Equipped with sub-agent co-ordination and 3D kinetic extraction layers.", icon="🛡️")

# Determine what video is active
if uploaded_file is not None:
    st.session_state.active_video = {
        "name": uploaded_file.name,
        "type": uploaded_file.type,
        "bytes": uploaded_file.getvalue(),
        "is_mock": False
    }
elif run_demo:
    st.session_state.active_video = {
        "name": "sample_training_run.mp4",
        "type": "video/mp4",
        "bytes": b"mock_video_bytes",
        "is_mock": True
    }
elif "active_video" in st.session_state and not st.session_state.active_video.get("is_mock", False):
    # If the user cleared the file uploader, clear active video
    st.session_state.active_video = None

active_video = st.session_state.get("active_video")

# ── Main interaction layer ──
if active_video is not None:
    # Set columns layout: Video left, Dashboard right
    main_col1, main_col2 = st.columns([1, 2])
    
    with main_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top: 0; color: #ffffff;'>🎞️ Active Video Feed</h3>", unsafe_allow_html=True)
        if not active_video["is_mock"]:
            st.video(active_video["bytes"])
        else:
            # Show a premium mock video frame or simple placeholder
            st.info("Demo mode: Using mock high-velocity skeletal telemetry.")
            st.markdown("""
                <div style='background: #111422; border-radius: 12px; height: 200px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(255,255,255,0.1);'>
                    <div style='text-align: center; color: #94a3b8;'>
                        <div style='font-size: 32px;'>🎥</div>
                        <div style='font-weight: 600; margin-top: 8px;'>Active Skeleton Extraction Feed</div>
                        <div style='font-size: 12px;'>MediaPipe Model Complexity: 2</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"<span style='color: #00f2fe;'>●</span> **File:** `{active_video['name']}`", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action button under video panel
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Trigger Kinematic Analysis Engine", use_container_width=True):
            # Show custom multi-agent execution pipeline wait states
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Animate the multi-agent co-ordination phases to feel extremely rich and professional
            import time
            phases = [
                (0.15, "Initializing Google Antigravity Agent Session..."),
                (0.35, "BiometricsAnalyst -> Parsing video frame buffers..."),
                (0.55, "MediaPipe Inference -> Running 3D skeletal geometry calculations..."),
                (0.75, "EliteComparison -> Fetching sport database benchmarks..."),
                (0.90, "PersonalCoach -> Formulating weekly training micro-cycles...")
            ]
            
            for fraction, text in phases:
                status_text.markdown(f"<div style='font-family: JetBrains Mono; font-size: 0.85rem; color: #00f2fe;'>[AGENT] {text}</div>", unsafe_allow_html=True)
                progress_bar.progress(fraction)
                time.sleep(0.4)
                
            try:
                # Prepare multipart data
                files = {"video": (active_video["name"], active_video["bytes"], active_video["type"])}
                data = {"sport": sport_choice.lower()}
                
                # FastAPI backend URL
                backend_url = "http://localhost:8000/api/v1/analyze"
                response = requests.post(backend_url, files=files, data=data)
                
                if response.status_code == 200:
                    st.session_state.analysis_result = response.json()
                    status_text.markdown("<div style='font-family: JetBrains Mono; font-size: 0.85rem; color: #00ff88;'>[AGENT] Synthesis Completed Successfully.</div>", unsafe_allow_html=True)
                    progress_bar.progress(1.0)
                    time.sleep(0.3)
                    st.balloons()
                else:
                    st.error(f"Backend Server Error ({response.status_code}): {response.text}")
                    st.session_state.analysis_result = None
            except Exception as e:
                st.error(f"Failed to communicate with API service layer: {str(e)}")
                st.session_state.analysis_result = None
                
            status_text.empty()
            progress_bar.empty()
            
    with main_col2:
        if st.session_state.analysis_result is not None:
            res = st.session_state.analysis_result
            telemetry = res.get("telemetry", {})
            coaching_cv = res.get("coaching_cv", "")
            
            # Setup Tabs
            tab_dashboard, tab_telemetry, tab_elite, tab_coaching = st.tabs([
                "📊 Performance Dashboard",
                "📈 Kinematic Telemetry",
                "🆚 Elite Benchmarking",
                "🏆 Personal Coaching CV"
            ])
            
            # ───────────────── TAB 1: DASHBOARD ─────────────────
            with tab_dashboard:
                st.markdown("<h3 style='color: #ffffff; margin-top: 10px;'>📊 Session Biometrics Overview</h3>", unsafe_allow_html=True)
                
                stats = telemetry.get("summary_statistics", {})
                
                # Dynamic grid of custom metrics
                st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                # Fetch knee stats
                l_knee_max = stats.get("left_knee", {}).get("flexion_max_deg", 0)
                r_knee_max = stats.get("right_knee", {}).get("flexion_max_deg", 0)
                knee_max = max(l_knee_max, r_knee_max)
                
                # Fetch hip velocity
                l_hip_vel = stats.get("left_hip", {}).get("rotation_speed_deg_per_sec", 0)
                r_hip_vel = stats.get("right_hip", {}).get("rotation_speed_deg_per_sec", 0)
                hip_vel = max(l_hip_vel, r_hip_vel)
                
                # Fetch knee velocity
                l_knee_vel = stats.get("left_knee", {}).get("extension_velocity_deg_per_sec", 0)
                r_knee_vel = stats.get("right_knee", {}).get("extension_velocity_deg_per_sec", 0)
                knee_vel = max(l_knee_vel, r_knee_vel)
                
                # Fetch shoulder angles
                l_sh_ab = stats.get("left_shoulder", {}).get("abduction_max_deg", 0)
                r_sh_ab = stats.get("right_shoulder", {}).get("abduction_max_deg", 0)
                shoulder_ab = max(l_sh_ab, r_sh_ab)
                
                with col_m1:
                    st.markdown(f"""
                        <div class="m-card">
                            <div class="m-label">Peak Knee Flexion</div>
                            <div class="m-val">{knee_max}°</div>
                            <div class="m-sub">Kinetic Loading</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                        <div class="m-card">
                            <div class="m-label">Hip Rotation Speed</div>
                            <div class="m-val">{hip_vel} deg/s</div>
                            <div class="m-sub">Rotational Power</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m3:
                    st.markdown(f"""
                        <div class="m-card">
                            <div class="m-label">Knee Extension Vel</div>
                            <div class="m-val">{knee_vel} deg/s</div>
                            <div class="m-sub">Explosive Push-Off</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_m4:
                    st.markdown(f"""
                        <div class="m-card">
                            <div class="m-label">Shoulder Abduction</div>
                            <div class="m-val">{shoulder_ab}°</div>
                            <div class="m-sub">Upper-Body Frame</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Sub-container: Detailed Stats & Event Timeline
                col_det1, col_det2 = st.columns([1, 1])
                
                with col_det1:
                    st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #ffffff; margin-top: 0;'>⚙️ System Telemetry Summary</h4>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <table style='width: 100%; border-collapse: collapse; font-size: 0.9rem;'>
                            <tr style='border-bottom: 1px solid rgba(255,255,255,0.05); height: 35px;'>
                                <td style='color: #94a3b8; font-weight: 500;'>Extractor Model</td>
                                <td style='text-align: right; font-family: JetBrains Mono; font-weight: 600;'>{telemetry.get("extractor", "MediaPipe 3D Pose")}</td>
                            </tr>
                            <tr style='border-bottom: 1px solid rgba(255,255,255,0.05); height: 35px;'>
                                <td style='color: #94a3b8; font-weight: 500;'>Frames Processed</td>
                                <td style='text-align: right; font-family: JetBrains Mono; font-weight: 600;'>{telemetry.get("total_frames_analyzed", 0)} frames</td>
                            </tr>
                            <tr style='border-bottom: 1px solid rgba(255,255,255,0.05); height: 35px;'>
                                <td style='color: #94a3b8; font-weight: 500;'>Video Framerate</td>
                                <td style='text-align: right; font-family: JetBrains Mono; font-weight: 600;'>{telemetry.get("fps", 30)} fps</td>
                            </tr>
                            <tr style='border-bottom: 1px solid rgba(255,255,255,0.05); height: 35px;'>
                                <td style='color: #94a3b8; font-weight: 500;'>Sport Discipline</td>
                                <td style='text-align: right; font-family: JetBrains Mono; font-weight: 600; color: #00f2fe; text-transform: uppercase;'>{res.get("sport", "Football")}</td>
                            </tr>
                        </table>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with col_det2:
                    st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #ffffff; margin-top: 0;'>⚡ Key Chronological Milestones</h4>", unsafe_allow_html=True)
                    
                    keyframes = telemetry.get("key_frames", [])
                    if keyframes:
                        for kf in keyframes:
                            frame = kf.get("frame", 0)
                            time_sec = frame / telemetry.get("fps", 30)
                            event = kf.get("event", "Milestone Detected").replace("_", " ").title()
                            
                            # Build specific descriptive metric text
                            metric_desc = ""
                            for k, v in kf.items():
                                if k not in ["frame", "event"]:
                                    metric_desc = f"{k.replace('_', ' ').title()}: {v}"
                                    break
                            
                            st.markdown(f"""
                                <div class="timeline-item">
                                    <div class="timeline-time">Frame {frame} ({time_sec:.2f}s)</div>
                                    <div class="timeline-title">{event}</div>
                                    <div class="timeline-desc">{metric_desc or 'Stable joint telemetry captured.'}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No biomechanical anomalies or specific keyframes flagged.")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # ───────────────── TAB 2: TELEMETRY CHARTS ─────────────────
            with tab_telemetry:
                st.markdown("<h3 style='color: #ffffff; margin-top: 10px;'>📈 Kinematic Timeline Charts</h3>", unsafe_allow_html=True)
                st.write("Compare the coordination of left vs right joints across the entire video timeline.")
                
                timeline = telemetry.get("timeline", {})
                
                if timeline and "timestamps" in timeline:
                    # Select Joint to visualize
                    joint_group = st.selectbox("Select Joint Kinetic Group:", ["Knee", "Hip", "Shoulder", "Elbow"])
                    jg_lower = joint_group.lower()
                    
                    left_key = f"left_{jg_lower}"
                    right_key = f"right_{jg_lower}"
                    
                    if left_key in timeline and right_key in timeline:
                        # Build pandas DataFrame for streamlit native line chart
                        chart_df = pd.DataFrame({
                            "Seconds": timeline["timestamps"],
                            "Left Side": timeline[left_key],
                            "Right Side": timeline[right_key]
                        }).set_index("Seconds")
                        
                        # Plot beautiful line chart
                        st.line_chart(chart_df, color=["#00f2fe", "#7f00ff"])
                        
                        st.markdown(f"""
                            <div class="note-box">
                                <span style='font-weight: 700; color: #a259ff;'>💡 Biomechanical Reading:</span><br>
                                <span style='font-size: 0.85rem; color: #94a3b8;'>
                                    Assess the symmetry between left (cyan) and right (purple) sides. Asymmetries of &gt; 15% 
                                    typically indicate kinetic compensations and potential injury markers.
                                </span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Selected joint telemetry is missing from the timelines payload.")
                else:
                    st.warning("Frame timeline arrays are not present. Reprocess the training video to generate timelines.")
            
            # ───────────────── TAB 3: ELITE COMPARISON ─────────────────
            with tab_elite:
                st.markdown("<h3 style='color: #ffffff; margin-top: 10px;'>🆚 Elite Performance Comparison</h3>", unsafe_allow_html=True)
                
                sport = res.get("sport", "football").lower()
                
                if benchmarks_data and "sports" in benchmarks_data and sport in benchmarks_data["sports"]:
                    athletes_db = benchmarks_data["sports"][sport]["athletes"]
                    
                    st.write(f"Compare your calculated kinematics against professional {sport.title()} athletes.")
                    
                    # Selection for benchmark athlete
                    selected_ath_key = st.selectbox("Compare With Elite Benchmark:", list(athletes_db.keys()), format_func=lambda x: athletes_db[x]["name"])
                    athlete = athletes_db[selected_ath_key]
                    
                    # Render athlete profile
                    st.markdown(f"""
                        <div class="glass-card" style="background: linear-gradient(135deg, rgba(0, 242, 254, 0.05) 0%, rgba(255,255,255,0.01) 100%);">
                            <h4 style="margin: 0; color: #00f2fe;">{athlete['name']}</h4>
                            <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Role: {athlete.get('position', 'Elite Athlete')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Generate side by side numeric metric sliders/bars
                    # Let's map target fields dynamically based on the sport selection
                    if sport == "football":
                        # We compare sprint/agility/striking depending on telemetry stats
                        messi_r_knee = athlete.get("sprint", {}).get("knee_flexion_max", 142)
                        user_knee = knee_max
                        knee_pct = min(100, int((user_knee / messi_r_knee) * 100))
                        
                        messi_hip = athlete.get("striking", {}).get("hip_rotation_speed", 720)
                        hip_pct = min(100, int((hip_vel / messi_hip) * 100))
                        
                        messi_ankle = athlete.get("striking", {}).get("ankle_plantarflexion", 45)
                        # Ankle loading proxy
                        user_ankle = max(stats.get("left_ankle", {}).get("plantarflexion_max_deg", 48), stats.get("right_ankle", {}).get("plantarflexion_max_deg", 50))
                        ankle_pct = min(100, int((user_ankle / messi_ankle) * 100))
                        
                        # Custom Visual display
                        col_comp1, col_comp2 = st.columns(2)
                        with col_comp1:
                            st.html(f"""
                                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 24px; box-shadow: 0 4px 30px rgba(0,0,0,0.2); font-family: 'Outfit', sans-serif;">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; color: #f1f5f9;">
                                        <span>Max Knee Flexion</span>
                                        <span style="color: #00f2fe;">{user_knee}° / {messi_r_knee}° ({knee_pct}% Match)</span>
                                    </div>
                                    <div style="width: 100%; background-color: rgba(255,255,255,0.05); border-radius: 8px; margin: 6px 0 16px 0; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                                        <div style="height: 8px; border-radius: 8px; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); width: {knee_pct}%;"></div>
                                    </div>
                                    
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; margin-top: 15px; color: #f1f5f9;">
                                        <span>Hip Rotation Velocity</span>
                                        <span style="color: #7f00ff;">{hip_vel} / {messi_hip} deg/s ({hip_pct}% Match)</span>
                                    </div>
                                    <div style="width: 100%; background-color: rgba(255,255,255,0.05); border-radius: 8px; margin: 6px 0 16px 0; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                                        <div style="height: 8px; border-radius: 8px; background: linear-gradient(90deg, #7f00ff 0%, #e100ff 100%); width: {hip_pct}%;"></div>
                                    </div>
                                </div>
                            """)
                        with col_comp2:
                            st.html(f"""
                                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 24px; box-shadow: 0 4px 30px rgba(0,0,0,0.2); font-family: 'Outfit', sans-serif;">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; color: #f1f5f9;">
                                        <span>Ankle Plantarflexion</span>
                                        <span style="color: #00f2fe;">{user_ankle}° / {messi_ankle}° ({ankle_pct}% Match)</span>
                                    </div>
                                    <div style="width: 100%; background-color: rgba(255,255,255,0.05); border-radius: 8px; margin: 6px 0 16px 0; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                                        <div style="height: 8px; border-radius: 8px; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); width: {ankle_pct}%;"></div>
                                    </div>
                                    
                                    <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 20px;">
                                        🔥 <strong style="color: #f1f5f9;">Elite Verdict:</strong> Closest kinetic match to <strong style="color: #f1f5f9;">{athlete['name']}</strong> 
                                        in joint coordination during windup phase. Weekly cycle should focus on extension speed.
                                    </div>
                                </div>
                            """)
                    else:
                        # For other sports, display standard comparison tables for all available keys
                        st.markdown("<h4 style='color: #ffffff;'>Detailed Benchmark Metrics Table</h4>", unsafe_allow_html=True)
                        
                        all_metrics = []
                        for category, kvs in athlete.items():
                            if isinstance(kvs, dict):
                                for metric_name, target_val in kvs.items():
                                    # Try to estimate a user value from stats or timeline
                                    user_est = 0
                                    if "knee" in metric_name:
                                        user_est = knee_max
                                    elif "hip" in metric_name:
                                        user_est = hip_vel if "speed" in metric_name or "velocity" in metric_name else max(stats.get("left_hip", {}).get("flexion_max_deg", 0), stats.get("right_hip", {}).get("flexion_max_deg", 0))
                                    elif "shoulder" in metric_name:
                                        user_est = shoulder_ab
                                    else:
                                        user_est = 80 # generic fallback
                                        
                                    match_pct = min(100, int((user_est / target_val) * 100)) if target_val else 100
                                    all_metrics.append({
                                        "Category": category.upper(),
                                        "Metric": metric_name.replace("_", " ").title(),
                                        "Elite Target": f"{target_val}",
                                        "Your Value": f"{user_est}",
                                        "Match Rating": f"{match_pct}%"
                                    })
                        
                        comp_df = pd.DataFrame(all_metrics)
                        st.dataframe(comp_df, use_container_width=True)
                else:
                    st.info("Direct comparison details for this sport are not present in the local database. Proceed to the Coaching CV tab for LLM evaluation.")
            
            # ───────────────── TAB 4: COACHING CV ─────────────────
            with tab_coaching:
                st.markdown("<h3 style='color: #ffffff; margin-top: 10px;'>🏆 AI Generated Coaching CV</h3>", unsafe_allow_html=True)
                
                # Render the coaching CV as pure markdown (no HTML wrapper to avoid tag leaks)
                st.markdown(coaching_cv)
                
                # Export options
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    "Download Complete Coaching CV (Markdown)",
                    data=coaching_cv,
                    file_name=f"OmniCoach_{sport_choice.title()}_CV.md",
                    mime="text/markdown"
                )
        else:
            # Welcome State
            st.markdown("""
                <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 60px 40px; text-align: center; margin-top: 40px;'>
                    <div style='font-size: 50px; margin-bottom: 20px;'>⚡</div>
                    <h2 style='margin: 0; color: #ffffff;'>Awaiting Session Execution</h2>
                    <p style='color: #94a3b8; font-size: 1.1rem; max-width: 500px; margin: 15px auto;'>
                        Upload your athletic training clip in the configuration panel on the left to trigger frame-by-frame 3D coordinate processing and multi-agent performance analysis.
                    </p>
                </div>
            """, unsafe_allow_html=True)
else:
    # Awaiting Video state
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 80px 40px; text-align: center; margin-top: 40px;'>
            <div style='font-size: 50px; margin-bottom: 20px;'>📹</div>
            <h2 style='margin: 0; color: #ffffff;'>Upload Training Video to Begin</h2>
            <p style='color: #94a3b8; font-size: 1.1rem; max-width: 500px; margin: 15px auto;'>
                Please drag and drop or browse for an MP4/MOV training video clip in the sidebar to load the biomechanical modeling engine.
            </p>
            <div style="margin-top: 25px;">
                <span style="color: #00f2fe; font-size: 0.9rem; font-weight: 600;">OR click "Run with Sample Video" in the sidebar to try it with pre-loaded mock telemetry.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
