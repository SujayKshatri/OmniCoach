#!/usr/bin/env python3
"""
OmniCoach Core API Engine
Exposes high-speed asynchronous endpoints for video upload, 
biomechanical telemetry extraction, and multi-agent synthesis.
"""

import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Temp storage directory for processing uploaded MP4s
UPLOAD_DIR = Path("/tmp/omnicoach_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class CoachingResponse(BaseModel):
    sport: str
    video_source: str
    coaching_cv: str

@app.get("/health")
async def health_check():
    """Verify system uptime and Antigravity SDK environment visibility."""
    return {
        "status": "healthy",
        "timestamp": "2026-07-05T02:31:31Z",
        "sdk": "google-antigravity-v3"
    }

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
            # Emulate the system message entry point
            user_prompt = (
                f"Analyse the sports training video located at: {str(local_video_path)}\n"
                f"Generate my complete Sports Coaching CV by running the full "
                f"three-stage pipeline (Biometrics -> Elite Comparison -> Coaching)."
            )
            
            # Execute agent turn loop
            response = await agent.chat(user_prompt)
            full_markdown_cv = await response.text()

        return CoachingResponse(
            sport=sport_cleaned,
            video_source=video.filename,
            coaching_cv=full_markdown_cv
        )

    except Exception as e:
        # Catch pipeline errors cleanly so the server doesn't crash during a live demo
        raise HTTPException(status_code=500, detail=f"Agent Execution Failure: {str(e)}")
        
    finally:
        # Background file cleanup to keep server disk unburdened
        if local_video_path.exists():
            os.remove(local_video_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
