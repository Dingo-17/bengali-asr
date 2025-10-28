#!/usr/bin/env python3
"""
Simple Bengali ASR API Server
Runs a lightweight FastAPI server for local testing with Whisper
"""

import os
import tempfile
import time
from pathlib import Path

try:
    import whisper
    import torch
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("Missing dependencies. Installing...")
    os.system("pip install openai-whisper fastapi uvicorn python-multipart torch")
    import whisper
    import torch
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn

# Initialize FastAPI
app = FastAPI(title="Bengali ASR API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model
print("Loading Whisper model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny", device=device)  # Use 'base' or 'small' for better accuracy
print(f"✓ Model loaded on {device}")

@app.get("/")
async def root():
    return {"message": "Bengali ASR API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model": "whisper-tiny", "device": device}

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """Transcribe audio file to Bengali text"""
    
    # Validate file
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
    file_ext = Path(audio.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    start_time = time.time()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await audio.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Transcribe using Whisper
        print(f"Transcribing: {audio.filename}")
        result = model.transcribe(
            tmp_path,
            language='bn',  # Bengali
            task='transcribe',
            fp16=False
        )
        
        # Calculate confidence (average of segment confidences if available)
        confidence = 0.9  # Default
        if 'segments' in result and result['segments']:
            confidences = [seg.get('no_speech_prob', 0.1) for seg in result['segments']]
            confidence = 1.0 - (sum(confidences) / len(confidences))
        
        # Clean up
        os.unlink(tmp_path)
        
        processing_time = (time.time() - start_time) * 1000  # ms
        
        return {
            "transcript_bangla": result['text'],
            "transcript_latin": None,  # Would need transliteration library
            "confidence": confidence,
            "tokens": result['text'].split(),
            "processing_time_ms": processing_time,
            "language": "bn"
        }
        
    except Exception as e:
        # Clean up on error
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎙️  Bengali ASR API Server")
    print("="*50)
    print(f"Model: Whisper Tiny (Bengali)")
    print(f"Device: {device}")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
