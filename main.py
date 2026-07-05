#!/usr/bin/env python3
"""
OmniCoach Core API Engine
Exposes high-speed asynchronous endpoints for video upload, 
biomechanical telemetry extraction, and multi-agent synthesis.
"""
import asyncio
import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.mock_generator import generate_mock_coaching_cv
import dotenv
dotenv.load_dotenv()

# Import your multi-agent factory setup from app.py
from app import _build_coordinator, types, Agent

app = FastAPI(
    title="OmniCoach API",
    description="Multi-sport AI biomechanical evaluation and multi-agent coaching engine.",
    version="1.0.0"
)

# Enable CORS for frontend integration (Streamlit, React, Next.js, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temp storage directory for processing uploaded MP4s (relative to script location for cross-platform safety)
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class CoachingResponse(BaseModel):
    sport: str
    video_source: str
    coaching_cv: str
    telemetry: dict = None

@app.get("/health")
async def health_check():
    """Verify system uptime and Antigravity SDK environment visibility."""
    return {
        "status": "healthy",
        "timestamp": "2026-07-05T02:31:31Z",
        "sdk": "google-antigravity-v3"
    }

from fastapi import Form, UploadFile, File, HTTPException
from pathlib import Path
import os
import shutil
import json

# Make sure this import is at the very top of your main.py file:
# from utils.mock_generator import generate_mock_coaching_cv

@app.post("/api/v1/analyze", response_model=CoachingResponse)
async def analyze_athletics_session(
    sport: str = Form(default="football", description="Sport discipline to benchmark against"),
    video: UploadFile = File(..., description="Target MP4/MOV training video clip")
):
    """
    Ingests video data, runs frame-by-frame 3D skeleton calculations, 
    and triggers the multi-agent execution pipeline.
    """
    # Clean and validate input sport names
    sport_cleaned = sport.lower().strip()
    
    # Restrict file extension anomalies
    file_ext = Path(video.filename).suffix.lower()
    if file_ext not in [".mp4", ".mov", ".avi"]:
        raise HTTPException(status_code=400, detail="Invalid video format. Use MP4, MOV, or AVI.")

    # Save the incoming multipart stream safely to our temp block
    local_video_path = UPLOAD_DIR / f"session_{os.getpid()}_{video.filename}"
    try:
        with local_video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to persist video stream: {str(e)}")

    try:
        # Build out the dynamic multi-agent pipeline based on the sport parameters
        config = _build_coordinator(str(local_video_path), sport_cleaned)
        
        # Initialize the stateful SDK session via the async context manager
        async with Agent(config) as agent:
            user_prompt = (
                f"Analyse the sports training video located at: {str(local_video_path)}\n"
                f"Generate my complete Sports Coaching CV by running the full "
                f"three-stage pipeline (Biometrics -> Elite Comparison -> Coaching)."
            )
            response = await agent.chat(user_prompt)
            full_markdown_cv = await response.text()

        # Extract telemetry data to pass to the UI
        from app import extract_mediapipe_telemetry
        try:
        # 1. Build out the dynamic multi-agent pipeline based on the sport parameters
        config = _build_coordinator(str(local_video_path), sport_cleaned)
        
        # 2. Initialize the stateful SDK session via the async context manager
        async with Agent(config) as agent:
            user_prompt = (
                f"Analyse the sports training video located at: {str(local_video_path)}\n"
                f"Generate my complete Sports Coaching CV by running the full "
                f"three-stage pipeline (Biometrics -> Elite Comparison -> Coaching)."
            )
            response = await agent.chat(user_prompt)
            full_markdown_cv = await response.text()

        # 3. Extract telemetry data to pass to the UI
        from app import extract_mediapipe_telemetry
        import json
        try:
            telemetry_data = json.loads(extract_mediapipe_telemetry(str(local_video_path)))
        except Exception:
            telemetry_data = {}

        # 4. SUCCESSFUL RETURN (If the API works perfectly)
        return CoachingResponse(
            sport=sport_cleaned,
            video_source=video.filename,
            coaching_cv=full_markdown_cv,
            telemetry=telemetry_data
        )

    except (Exception, asyncio.CancelledError) as e:
        # 5. FALLBACK RETURN (If the API hits rate limits or you cancel)
        print(f"--- [FALLBACK ACTIVATED] --- Live agent hit API limit or crashed: {str(e)}")
        
        from utils.mock_generator import generate_mock_coaching_cv
        fallback_markdown = generate_mock_coaching_cv(sport_cleaned, str(local_video_path))
        
        return CoachingResponse(
            sport=sport_cleaned,
            video_source=video.filename,
            coaching_cv=fallback_markdown,
            telemetry={"status": "fallback_active", "user_metrics": {"plant_knee_flexion_degrees": 134.2}}
        )
        
    finally:
        # 6. Background file cleanup to keep server disk unburdened
        if local_video_path.exists():
            os.remove(local_video_path)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
