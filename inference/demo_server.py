"""
Ultra-lightweight demo server for Render.com free tier.
No model dependencies - pure demo mode.
"""

import os
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bengali ASR API - Demo",
    description="Demo API for testing (Free Tier)",
    version="1.0.0-demo"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Bengali ASR Demo API",
        "status": "online",
        "mode": "demo",
        "tier": "free",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check."""
    return {
        "status": "healthy",
        "mode": "demo",
        "tier": "free",
        "message": "Demo mode - returns mock transcriptions",
        "limitations": {
            "max_file_size_mb": 5.0,
            "max_duration_seconds": 30,
            "ram": "512MB",
            "note": "Upgrade for actual transcription"
        }
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Demo transcription endpoint."""
    start = time.time()
    
    # Validate file
    if not file.filename:
        raise HTTPException(400, "No file provided")
    
    # Read file (just to validate upload works)
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > 5 * 1024 * 1024:
        raise HTTPException(400, f"File too large: {file_size/(1024*1024):.1f}MB (max 5MB)")
    
    processing_time = (time.time() - start) * 1000
    
    # Return demo response
    return {
        "transcript_bangla": "আমি বাংলায় গান গাই (Demo Mode)",
        "confidence": 0.95,
        "processing_time_ms": processing_time,
        "demo_mode": True,
        "message": "FREE TIER DEMO: This is a sample response. Upgrade for actual transcription.",
        "file_info": {
            "filename": file.filename,
            "size_mb": round(file_size / (1024*1024), 2)
        }
    }

@app.get("/info")
def info():
    """Service information."""
    return {
        "tier": "free",
        "mode": "demo",
        "ram": "512MB",
        "features": {
            "health_check": True,
            "file_upload": True,
            "actual_transcription": False,
            "reason": "Limited RAM on free tier"
        },
        "upgrade": "https://render.com/pricing"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("demo_server:app", host="0.0.0.0", port=port, workers=1)
