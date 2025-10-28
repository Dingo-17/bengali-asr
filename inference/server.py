"""
FastAPI server for Bengali ASR inference.

This server provides REST API endpoints for:
1. Audio transcription (Bengali script)
2. Phonetic transcription (IPA/Latin)
3. Health check and monitoring

Endpoints:
- POST /transcribe: Transcribe audio file
- POST /transcribe/phonetic: Transcribe with phonetic output
- GET /health: Health check

Usage:
    uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4

Author: BRAC Data Science Team
Date: October 2025
"""

import os
import tempfile
import time
from pathlib import Path
from typing import Optional, List
from enum import Enum

import torch
import librosa
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import model loaders
from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    WhisperProcessor,
    WhisperForConditionalGeneration
)

# Import transliteration (optional)
try:
    from transliterate import bengali_to_latin, latin_to_ipa
    TRANSLITERATION_AVAILABLE = True
except ImportError:
    TRANSLITERATION_AVAILABLE = False
    print("Warning: transliterate module not found. Phonetic features disabled.")


# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "./models/wav2vec2_bengali/checkpoint-best")
MODEL_TYPE = os.getenv("MODEL_TYPE", "wav2vec2")  # "wav2vec2" or "whisper"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_AUDIO_DURATION = 60  # seconds
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a"}


# Pydantic models
class TranscriptionResponse(BaseModel):
    transcript_bangla: str
    transcript_latin: Optional[str] = None
    confidence: float
    tokens: List[str]
    processing_time_ms: float
    language: str = "bn"


class PhoneticResponse(BaseModel):
    transcript_bangla: str
    transcript_latin: str
    transcript_ipa: Optional[str] = None
    confidence: float
    tokens: List[str]
    processing_time_ms: float


class OutputFormat(str, Enum):
    BANGLA = "bangla"
    LATIN = "latin"
    IPA = "ipa"


# Initialize FastAPI app
app = FastAPI(
    title="Bengali ASR API",
    description="Automatic Speech Recognition for Bengali dialects",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Global model variables (loaded at startup)
processor = None
model = None


@app.on_event("startup")
async def load_model():
    """Load model at startup."""
    global processor, model
    
    print(f"Loading {MODEL_TYPE} model from {MODEL_PATH}...")
    print(f"Using device: {DEVICE}")
    
    try:
        if MODEL_TYPE == "wav2vec2":
            processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
            model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH).to(DEVICE)
        elif MODEL_TYPE == "whisper":
            processor = WhisperProcessor.from_pretrained(MODEL_PATH)
            model = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
        else:
            raise ValueError(f"Unknown model type: {MODEL_TYPE}")
        
        model.eval()
        print("✓ Model loaded successfully!")
        
    except Exception as e:
        print(f"✗ Error loading model: {str(e)}")
        raise


def transcribe_audio_wav2vec2(audio_path: str) -> tuple[str, float]:
    """
    Transcribe audio using Wav2Vec2.
    
    Returns:
        Tuple of (transcript, confidence_score)
    """
    # Load audio
    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    
    # Process
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        logits = model(inputs.input_values.to(DEVICE)).logits
    
    # Decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    # Calculate confidence (average of max probabilities)
    probs = torch.nn.functional.softmax(logits, dim=-1)
    max_probs = torch.max(probs, dim=-1).values
    confidence = float(max_probs.mean().cpu())
    
    return transcription, confidence


def transcribe_audio_whisper(audio_path: str) -> tuple[str, float]:
    """
    Transcribe audio using Whisper.
    
    Returns:
        Tuple of (transcript, confidence_score)
    """
    # Load audio
    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    
    # Process
    input_features = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_features.to(DEVICE)
    
    # Generate
    with torch.no_grad():
        predicted_ids = model.generate(input_features)
    
    # Decode
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    
    # Whisper doesn't provide confidence directly, return 0.9 as placeholder
    confidence = 0.9
    
    return transcription, confidence


def validate_audio_file(file: UploadFile) -> None:
    """Validate uploaded audio file."""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size (100MB max)
    if file.size and file.size > 100 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size: 100MB"
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Bengali ASR API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "transcribe": "/transcribe",
            "phonetic": "/transcribe/phonetic",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_type": MODEL_TYPE,
        "model_loaded": model is not None,
        "device": DEVICE
    }


@app.post("/transcribe", response_model=TranscriptionResponse)
@limiter.limit("10/minute")
async def transcribe(
    request: Request,
    audio: UploadFile = File(...),
    language: str = Form(default="bn"),
    include_latin: bool = Form(default=False)
):
    """
    Transcribe audio file to Bengali text.
    
    Args:
        audio: Audio file (WAV, MP3, OGG, FLAC, M4A)
        language: Language code (default: "bn")
        include_latin: Include Latin transliteration in response
    
    Returns:
        Transcription result
    """
    start_time = time.time()
    
    # Validate file
    validate_audio_file(audio)
    
    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as tmp_file:
        content = await audio.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Check audio duration
        duration = librosa.get_duration(path=tmp_path)
        if duration > MAX_AUDIO_DURATION:
            raise HTTPException(
                status_code=400,
                detail=f"Audio too long. Maximum duration: {MAX_AUDIO_DURATION}s"
            )
        
        # Transcribe
        if MODEL_TYPE == "wav2vec2":
            transcript, confidence = transcribe_audio_wav2vec2(tmp_path)
        else:
            transcript, confidence = transcribe_audio_whisper(tmp_path)
        
        # Tokenize
        tokens = transcript.split()
        
        # Optional Latin transliteration
        transcript_latin = None
        if include_latin and TRANSLITERATION_AVAILABLE:
            transcript_latin = bengali_to_latin(transcript)
        
        processing_time = (time.time() - start_time) * 1000
        
        return TranscriptionResponse(
            transcript_bangla=transcript,
            transcript_latin=transcript_latin,
            confidence=confidence,
            tokens=tokens,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/transcribe/phonetic", response_model=PhoneticResponse)
@limiter.limit("10/minute")
async def transcribe_phonetic(
    request: Request,
    audio: UploadFile = File(...),
    output_format: OutputFormat = Form(default=OutputFormat.LATIN)
):
    """
    Transcribe audio with phonetic output (IPA or Latin).
    
    Args:
        audio: Audio file
        output_format: Output format ("bangla", "latin", or "ipa")
    
    Returns:
        Transcription with phonetic output
    """
    if not TRANSLITERATION_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="Transliteration not available. Install epitran and aksharamukha."
        )
    
    start_time = time.time()
    
    # Validate file
    validate_audio_file(audio)
    
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as tmp_file:
        content = await audio.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Transcribe
        if MODEL_TYPE == "wav2vec2":
            transcript, confidence = transcribe_audio_wav2vec2(tmp_path)
        else:
            transcript, confidence = transcribe_audio_whisper(tmp_path)
        
        # Transliterate
        transcript_latin = bengali_to_latin(transcript)
        transcript_ipa = None
        
        if output_format == OutputFormat.IPA:
            transcript_ipa = latin_to_ipa(transcript_latin)
        
        # Tokenize
        tokens = transcript.split()
        
        processing_time = (time.time() - start_time) * 1000
        
        return PhoneticResponse(
            transcript_bangla=transcript,
            transcript_latin=transcript_latin,
            transcript_ipa=transcript_ipa,
            confidence=confidence,
            tokens=tokens,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("Bengali ASR Inference Server")
    print("="*60)
    print(f"Model: {MODEL_PATH}")
    print(f"Model type: {MODEL_TYPE}")
    print(f"Device: {DEVICE}")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
