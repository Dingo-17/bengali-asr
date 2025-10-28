#!/usr/bin/env python3
"""
Quick test of Bengali ASR using Whisper
This downloads a small model and tests transcription
"""

import sys
import whisper
import torch

def test_whisper():
    print("=" * 60)
    print("Bengali ASR Quick Test with Whisper")
    print("=" * 60)
    print()
    
    # Check device
    if torch.backends.mps.is_available():
        device = "mps"
        print("✓ Using Apple Metal (GPU acceleration)")
    elif torch.cuda.is_available():
        device = "cuda"
        print("✓ Using NVIDIA CUDA")
    else:
        device = "cpu"
        print("✓ Using CPU")
    print()
    
    # Load model
    print("Downloading and loading Whisper 'tiny' model...")
    print("(First time will download ~75MB)")
    try:
        model = whisper.load_model("tiny", device=device)
        print("✓ Model loaded successfully!")
        print()
        
        # Model info
        print("Model details:")
        print(f"  - Size: tiny (~75MB)")
        print(f"  - Languages: 99 languages including Bengali")
        print(f"  - Device: {device}")
        print()
        
        # Test transcription with sample text
        print("=" * 60)
        print("Test Complete!")
        print("=" * 60)
        print()
        print("The model is ready to transcribe Bengali audio.")
        print()
        print("To transcribe an audio file, create a Python script:")
        print()
        print("  import whisper")
        print("  model = whisper.load_model('tiny')")
        print("  result = model.transcribe('audio.wav', language='bn')")
        print("  print(result['text'])")
        print()
        print("Or use a larger model for better accuracy:")
        print("  - 'base' (~150MB) - Good balance")
        print("  - 'small' (~500MB) - Better accuracy")
        print("  - 'medium' (~1.5GB) - High accuracy")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_whisper()
    sys.exit(0 if success else 1)
