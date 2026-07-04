#!/usr/bin/env python3

import streamlit as st
import requests

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="OmniCoach",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#0F172A;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

h1,h2,h3{
    color:white;
}

.hero{
    padding:25px;
    border-radius:15px;
    background:linear-gradient(90deg,#2563EB,#06B6D4);
    color:white;
    text-align:center;
    margin-bottom:20px;
}

.metric{
    background:#1E293B;
    padding:18px;
    border-radius:12px;
    text-align:center;
    color:white;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#06B6D4,#2563EB);
    color:white;
    border:none;
    border-radius:10px;
    font-size:17px;
    font-weight:bold;
    padding:10px;
}

.stButton>button:hover{
    background:linear-gradient(90deg,#2563EB,#06B6D4);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------

st.markdown("""
<div class="hero">
<h1>⚡ OmniCoach</h1>
<h4>AI Biomechanical Performance Analysis</h4>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙️ Settings")

sport = st.sidebar.selectbox(
    "Select Sport",
    ["Football","Basketball","Tennis","Cricket","Athletics"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Video",
    type=["mp4","mov","avi"]
)

st.sidebar.markdown("---")
st.sidebar.success("AI Ready")

# -----------------------------
# Metrics
# -----------------------------

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric">
    <h3>🤖 AI Agents</h3>
    <h2>6</h2>
    </div>
    """,unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric">
    <h3>🏅 Sport</h3>
    <h2>{sport}</h2>
    </div>
    """,unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric">
    <h3>📈 Status</h3>
    <h2>Ready</h2>
    </div>
    """,unsafe_allow_html=True)

st.write("")

# -----------------------------
# Main Layout
# -----------------------------

left,right = st.columns([1,1])

# -----------------------------
# Left Panel
# -----------------------------

with left:

    st.subheader("🎥 Video Preview")

    if uploaded_file:

        st.video(uploaded_file)

        st.success("Video Uploaded Successfully")

    else:

        st.info("Upload a video from the sidebar.")

# -----------------------------
# Right Panel
# -----------------------------

with right:

    st.subheader("📊 Coaching Report")

    if uploaded_file:

        if st.button("🚀 Analyze Performance"):

            progress = st.progress(0)

            for i in range(100):
                progress.progress(i+1)

            try:

                files = {
                    "video": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                data = {
                    "sport": sport.lower()
                }

                response = requests.post(
                    "http://localhost:8000/api/v1/analyze",
                    files=files,
                    data=data
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Analysis Complete ✅")

                    st.balloons()

                    with st.expander("📄 Coaching CV", expanded=True):
                        st.markdown(result["coaching_cv"])

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(e)

    else:

        st.info("Waiting for video...")

# -----------------------------
# Footer
# -----------------------------

st.write("---")

st.caption("⚡ OmniCoach • Powered by Google AI + MediaPipe + Streamlit")
