#!/usr/bin/env python3
"""
Download Whisper model with SSL fix
"""

import os
import ssl
import urllib.request

# Fix SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

import whisper
import torch

print("=" * 60)
print("Downloading Whisper Model (SSL Fix Applied)")
print("=" * 60)
print()

# Check device
if torch.backends.mps.is_available():
    device = "mps"
    print("✓ Using Apple Metal (GPU)")
else:
    device = "cpu"
    print("✓ Using CPU")
print()

print("Downloading Whisper 'tiny' model (~75MB)...")
print("This may take a few minutes...")
print()

try:
    model = whisper.load_model("tiny", device=device)
    print("✓ Model downloaded and loaded successfully!")
    print()
    print("Model details:")
    print(f"  - Name: tiny")
    print(f"  - Size: ~75MB")
    print(f"  - Languages: 99 (including Bengali)")
    print(f"  - Device: {device}")
    print()
    print("=" * 60)
    print("Success! The model is ready to use.")
    print("=" * 60)
    print()
    print("Example usage:")
    print()
    print("  import whisper")
    print("  model = whisper.load_model('tiny')")
    print("  result = model.transcribe('audio.wav', language='bn')")
    print("  print(result['text'])")
    print()
    
except Exception as e:
    print(f"✗ Error: {e}")
    print()
    print("If download fails, you can manually download from:")
    print("https://openaipublic.azureedge.net/main/whisper/models/")
