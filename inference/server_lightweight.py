"""
Lightweight FastAPI server for Bengali ASR - Optimized for Free Tier (Render.com)

This version uses minimal dependencies and lazy loading to work within 512MB RAM limits.
For demo/testing purposes only. For production, upgrade to a paid tier or use a lighter model.

Author: BRAC Data Science Team
Date: October 2025
"""

import os
import tempfile
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# Configuration
MAX_AUDIO_DURATION = 30  # seconds (reduced for free tier)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB (reduced for free tier)
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a"}


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool
    device: str
    tier: str
    limitations: dict


class TranscriptionResponse(BaseModel):
    transcript_bangla: str
    confidence: float
    processing_time_ms: float
    demo_mode: bool
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="Bengali ASR API - Free Tier",
    description="Bengali Automatic Speech Recognition API (Demo Mode for Free Tier)",
    version="1.0.0-free",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global variable for lazy model loading
_model = None
_processor = None


def get_model():
    """
    Lazy load model only when needed.
    For free tier, we'll use a mock model to demonstrate functionality.
    """
    global _model, _processor
    
    if _model is None:
        # For free tier demo, we'll return a mock transcription
        # In production with more RAM, you'd load the actual model here
        print("INFO: Running in DEMO MODE (Free Tier - Limited RAM)")
        print("INFO: For production transcription, upgrade to a paid tier")
        _model = "demo_mode"
        _processor = "demo_mode"
    
    return _model, _processor


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Bengali ASR API - Free Tier Demo",
        "status": "online",
        "docs": "/docs",
        "health": "/health",
        "tier": "free",
        "note": "Demo mode - upgrade for full transcription"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return HealthResponse(
        status="ok",
        message="Service is running (Demo Mode - Free Tier)",
        model_loaded=True,
        device="cpu",
        tier="free",
        limitations={
            "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
            "max_duration_seconds": MAX_AUDIO_DURATION,
            "mode": "demo",
            "ram": "512MB",
            "note": "Upgrade to paid tier for full model transcription"
        }
    )


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
):
    """
    Transcribe Bengali audio file.
    
    FREE TIER DEMO MODE:
    - Returns sample transcription for testing
    - Validates file format and size
    - For actual transcription, upgrade to paid tier with more RAM
    
    Args:
        file: Audio file (wav, mp3, ogg, flac, m4a)
    
    Returns:
        TranscriptionResponse with demo transcription
    """
    start_time = time.time()
    
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file to check size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large: {file_size / (1024*1024):.2f}MB. Max: {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        # Save to temp file (for validation)
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        try:
            # Demo mode response
            # In production with more RAM, you'd process the audio here
            processing_time = (time.time() - start_time) * 1000
            
            # Sample Bengali transcription for demo
            demo_transcription = "আমি বাংলায় গান গাই (Demo Mode - Free Tier)"
            
            return TranscriptionResponse(
                transcript_bangla=demo_transcription,
                confidence=0.95,
                processing_time_ms=processing_time,
                demo_mode=True,
                message="FREE TIER DEMO: Upgrade to paid tier for actual transcription. This is a sample response."
            )
        
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


@app.get("/info")
async def get_info():
    """
    Get information about the free tier limitations and upgrade options.
    """
    return {
        "tier": "free",
        "mode": "demo",
        "limitations": {
            "ram": "512 MB",
            "model": "Demo mode (no actual transcription)",
            "max_file_size": f"{MAX_FILE_SIZE / (1024*1024)} MB",
            "max_duration": f"{MAX_AUDIO_DURATION} seconds",
            "sleeps_after": "15 minutes of inactivity"
        },
        "upgrade_benefits": {
            "starter_7_per_month": {
                "ram": "1 GB+",
                "model": "Full Wav2Vec2/Whisper model",
                "no_sleep": True,
                "faster_cpu": True,
                "actual_transcription": True
            }
        },
        "message": "This free tier demonstrates API structure. Upgrade for actual Bengali transcription.",
        "upgrade_url": "https://render.com/pricing"
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": "Endpoint not found. Check /docs for available endpoints."
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please try again later.",
            "tier": "free",
            "note": "Free tier has limited resources. Consider upgrading."
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "server_lightweight:app",
        host="0.0.0.0",
        port=port,
        workers=1,  # Single worker for free tier
        log_level="info"
    )
