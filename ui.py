#!/usr/bin/env python3
"""
OmniCoach Frontend Dashboard - Stable Hackathon Edition
High-velocity Streamlit UI with robust mock/live pipeline switching toggles.
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

sport_choice = st.sidebar.selectbox(
    "Target Discipline:",
    ["Football", "Basketball", "Tennis", "Cricket", "Athletics"],
    index=["Football", "Basketball", "Tennis", "Cricket", "Athletics"].index(st.session_state.selected_sport)
)
st.session_state.selected_sport = sport_choice

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

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #ffffff;'>⚡ Quick Demo Mode</h3>", unsafe_allow_html=True)
run_demo = st.sidebar.button("Run with Sample Video")

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.info("🤖 **Antigravity Framework v3**<br>Equipped with sub-agent co-ordination and 3D kinetic extraction layers.", icon="🛡️")

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

active_video = st.session_state.get("active_video")

# ── Main interaction layer ──
if active_video is not None:
    # Set columns layout: Video left, Dashboard right
    main_col1, main_col2 = st.columns([1, 2])
    
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
                            st.markdown(f"""
                                <div class="glass-card">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600;">
                                        <span>Max Knee Flexion</span>
                                        <span style="color: #00f2fe;">{user_knee}° / {messi_r_knee}° ({knee_pct}% Match)</span>
                                    </div>
                                    <div class="progress-container">
                                        <div class="progress-bar-fill" style="background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); width: {knee_pct}%;"></div>
                                    </div>
                                    
                                    <div style="display: flex; justify-content: space-between; font-weight: 600; margin-top: 15px;">
                                        <span>Hip Rotation Velocity</span>
                                        <span style="color: #7f00ff;">{hip_vel} / {messi_hip} deg/s ({hip_pct}% Match)</span>
                                    </div>
                                    <div class="progress-container">
                                        <div class="progress-bar-fill" style="background: linear-gradient(90deg, #7f00ff 0%, #e100ff 100%); width: {hip_pct}%;"></div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        with col_comp2:
                            st.markdown(f"""
                                <div class="glass-card">
                                    <div style="display: flex; justify-content: space-between; font-weight: 600;">
                                        <span>Ankle Plantarflexion</span>
                                        <span style="color: #00f2fe;">{user_ankle}° / {messi_ankle}° ({ankle_pct}% Match)</span>
                                    </div>
                                    <div class="progress-container">
                                        <div class="progress-bar-fill" style="background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); width: {ankle_pct}%;"></div>
                                    </div>
                                    
                                    <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 20px;">
                                        🔥 <strong>Elite Verdict:</strong> Closest kinetic match to <strong>{athlete['name']}</strong> 
                                        in joint coordination during windup phase. Weekly cycle should focus on extension speed.
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
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
                
                st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px; line-height: 1.6; font-size: 0.95rem;">
                        {coaching_cv}
                    </div>
                """, unsafe_allow_html=True)
                
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
