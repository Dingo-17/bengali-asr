#!/bin/bash
# Test workflow script for Bengali ASR system
# This script demonstrates the complete pipeline with sample data

set -e  # Exit on error

echo "=========================================="
echo "Bengali ASR Test Workflow"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate virtual environment
echo -e "${BLUE}Step 1: Activating virtual environment${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Check if sample data exists
echo -e "${BLUE}Step 2: Verifying sample data${NC}"
if [ -f "data/raw/sample_bengali/manifest.txt" ]; then
    echo -e "${GREEN}✓ Sample data found${NC}"
    echo "Sample transcripts:"
    head -n 5 data/raw/sample_bengali/manifest.txt
else
    echo -e "${RED}✗ Sample data not found. Run: python3 data/download_simple.py${NC}"
    exit 1
fi
echo ""

# Install FFmpeg reminder
echo -e "${BLUE}Step 3: Checking for FFmpeg${NC}"
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓ FFmpeg installed: $(ffmpeg -version | head -n1)${NC}"
else
    echo -e "${RED}⚠️  FFmpeg not found${NC}"
    echo "   Install with: brew install ffmpeg"
    echo "   (Optional, but recommended for audio processing)"
fi
echo ""

# Display next steps
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Install FFmpeg (if not already installed):"
echo "   ${BLUE}brew install ffmpeg${NC}"
echo ""
echo "2. Create sample audio files (or skip to use pre-trained models):"
echo "   Place .wav files in: data/raw/sample_bengali/"
echo "   Named: sample_001.wav, sample_002.wav, sample_003.wav"
echo ""
echo "3. Preprocess the data:"
echo "   ${BLUE}python3 data/preprocess.py --input_dirs data/raw/sample_bengali --output_dir data/processed${NC}"
echo ""
echo "4. Train a model (or download pre-trained):"
echo "   ${BLUE}python3 train/wav2vec2_finetune.py --train_data data/processed/train.tsv --valid_data data/processed/valid.tsv --output_dir models/wav2vec2_bengali${NC}"
echo ""
echo "5. Run the inference server:"
echo "   ${BLUE}python3 inference/server.py${NC}"
echo ""
echo "6. Test the API:"
echo "   ${BLUE}curl -X POST 'http://localhost:8000/transcribe' -F 'audio=@sample.wav'${NC}"
echo ""
echo "=========================================="
echo "Quick Test (Using Pre-trained Model):"
echo "=========================================="
echo ""
echo "If you want to skip training and use a pre-trained model:"
echo ""
echo "1. Download a pre-trained Bengali model:"
echo "   From Hugging Face: https://huggingface.co/models?language=bn&pipeline_tag=automatic-speech-recognition"
echo ""
echo "2. Or use Whisper directly:"
echo "   ${BLUE}python3 -c \"import whisper; model = whisper.load_model('small'); result = model.transcribe('sample.wav', language='bn'); print(result['text'])\"${NC}"
echo ""
echo "=========================================="
echo "Documentation:"
echo "=========================================="
echo "- README.md           - Full project documentation"
echo "- QUICKSTART_FIXED.md - Corrected quick start commands"
echo "- TROUBLESHOOTING.md  - Solutions to common problems"
echo ""
echo -e "${GREEN}Setup complete! Virtual environment is active.${NC}"
