#!/bin/bash
# Setup script for Bengali Dialect Transcription Project
# This script handles initial setup on macOS/Linux

set -e  # Exit on error

echo "========================================"
echo "Bengali ASR Project Setup"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "requirements.txt" ]; then
    echo "Error: Please run this script from the BracV1 directory"
    echo "Usage: cd BracV1 && bash setup.sh"
    exit 1
fi

# Detect Python command (python3 on macOS, python on some Linux)
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.8+ from:"
    echo "  - https://www.python.org/downloads/"
    echo "  - Or use: brew install python3"
    exit 1
fi

echo "✓ Found Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version check passed"
echo ""

# Create virtual environment
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists: $VENV_DIR"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing old virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "Using existing virtual environment"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing Python dependencies..."
echo "This may take 5-10 minutes depending on your internet speed..."
echo ""

pip install -r requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/augmented
mkdir -p data/manifests
mkdir -p data/brac_dialect
mkdir -p data/brac_corrections
mkdir -p models
mkdir -p logs
mkdir -p eval/results
mkdir -p inference/logs

echo "✓ Directories created"
echo ""

# Check for optional dependencies
echo "Checking optional dependencies..."

# Check for FFmpeg (required for audio processing)
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg found"
else
    echo "⚠️  FFmpeg not found (recommended for audio processing)"
    echo "   Install with: brew install ffmpeg"
fi

# Check for CUDA (for GPU support)
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU detected"
    nvidia-smi --query-gpu=name --format=csv,noheader
else
    echo "ℹ️  No NVIDIA GPU detected (CPU-only mode)"
fi

echo ""
echo "========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "2. Download datasets:"
echo "   cd data"
echo "   python3 download_datasets.py --datasets openslr common_voice bengaliai --output ./raw"
echo ""
echo "3. Preprocess data:"
echo "   python3 preprocess.py \\"
echo "     --input_dirs ./raw/openslr_slr53 ./raw/common_voice_bn \\"
echo "     --output_dir ./processed \\"
echo "     --speaker_split"
echo ""
echo "4. Train a model:"
echo "   cd ../train"
echo "   python3 wav2vec2_finetune.py \\"
echo "     --train_data ../data/processed/train.tsv \\"
echo "     --valid_data ../data/processed/valid.tsv \\"
echo "     --output_dir ../models/wav2vec2_bengali"
echo ""
echo "5. Start inference server:"
echo "   cd ../inference"
echo "   python3 server.py"
echo ""
echo "For more details, see README.md"
echo ""
echo "Happy transcribing! 🎙️"
echo ""
