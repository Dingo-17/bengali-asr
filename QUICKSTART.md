# 🚀 Quick Start Guide for macOS

This guide will help you get the Bengali ASR system running on your Mac.

## Prerequisites

### 1. Install Python 3.8+

Check if Python is installed:
```bash
python3 --version
```

If not installed, install via Homebrew:
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

### 2. Install FFmpeg (for audio processing)

```bash
brew install ffmpeg
```

### 3. (Optional) Install Git LFS for large files

```bash
brew install git-lfs
git lfs install
```

## Installation

### Step 1: Navigate to the project directory

```bash
cd /Users/digantohaque/python/BracV1
```

### Step 2: Run the setup script

```bash
# Make the script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Create necessary directories

### Step 3: Activate the virtual environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

## Running the System

### Option 1: Quick Test (CPU-only, Small Dataset)

For testing without downloading large datasets:

1. **Create a test audio file** (or use your own `.wav` file)

2. **Start the inference server:**
```bash
cd inference

# Set environment variable to use a pre-trained model from Hugging Face
export MODEL_PATH="facebook/wav2vec2-large-xlsr-53"
export MODEL_TYPE="wav2vec2"

# Start server
python3 server.py
```

3. **Test the API** (in a new terminal):
```bash
# Test health endpoint
curl http://localhost:8000/health

# Transcribe audio (replace with your audio file)
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@/path/to/your/audio.wav" \
  -F "language=bn"
```

### Option 2: Full Pipeline (Training from Scratch)

#### Step 1: Download datasets

```bash
cd /Users/digantohaque/python/BracV1/data

# Download all datasets (this will take time and ~200GB space)
python3 download_datasets.py --datasets all --output ./raw
```

**Note:** You may need to:
- Create a Hugging Face account at https://huggingface.co/
- Accept dataset terms for Common Voice
- Login: `huggingface-cli login`

#### Step 2: Preprocess data

```bash
python3 preprocess.py \
  --input_dirs ./raw/openslr_slr53 ./raw/common_voice_bn \
  --output_dir ./processed \
  --sample_rate 16000 \
  --speaker_split
```

#### Step 3: Train model

```bash
cd ../train

# For CPU training (slow, for testing only)
python3 wav2vec2_finetune.py \
  --train_data ../data/processed/train.tsv \
  --valid_data ../data/processed/valid.tsv \
  --output_dir ../models/wav2vec2_bengali \
  --batch_size 2 \
  --gradient_accumulation_steps 8 \
  --num_epochs 5

# For GPU training (if you have NVIDIA GPU)
python3 wav2vec2_finetune.py \
  --train_data ../data/processed/train.tsv \
  --valid_data ../data/processed/valid.tsv \
  --output_dir ../models/wav2vec2_bengali \
  --batch_size 8 \
  --mixed_precision
```

#### Step 4: Evaluate

```bash
cd ../eval

python3 eval_wer_cer.py \
  --model_path ../models/wav2vec2_bengali/checkpoint-best \
  --test_data ../data/processed/test.tsv \
  --output_dir ./results \
  --detailed_analysis
```

#### Step 5: Deploy

```bash
cd ../inference

# Option A: Run directly with Python
python3 server.py

# Option B: Run with Docker
docker-compose -f docker-compose.cpu.yml up
```

### Option 3: Frontend Development

```bash
cd /Users/digantohaque/python/BracV1/frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

Open http://localhost:5173 in your browser.

## Troubleshooting

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python` on macOS

### Issue: "pip: command not found"
**Solution:** Use `pip3` or `python3 -m pip`

### Issue: "CUDA not available"
**Solution:** Normal on Mac (M1/M2) - the system will use CPU. For GPU, use:
```bash
# For Apple Silicon (M1/M2)
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### Issue: Import errors for packages
**Solution:** Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** Either kill the existing process or use a different port:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn inference.server:app --port 8001
```

### Issue: Out of memory during training
**Solution:** Reduce batch size:
```bash
python3 wav2vec2_finetune.py \
  --batch_size 1 \
  --gradient_accumulation_steps 16
```

## Minimal Test Example

If you just want to test the system quickly:

```bash
cd /Users/digantohaque/python/BracV1

# Activate environment
source venv/bin/activate

# Create a simple test script
cat > test_transcribe.py << 'EOF'
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import librosa
import torch

# Load pre-trained model
model_name = "facebook/wav2vec2-large-xlsr-53"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

# Load audio
audio, sr = librosa.load("path/to/your/audio.wav", sr=16000)

# Process
inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)

# Transcribe
with torch.no_grad():
    logits = model(inputs.input_values).logits

predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]

print(f"Transcription: {transcription}")
EOF

# Run test (replace with your audio file path)
python3 test_transcribe.py
```

## Next Steps

1. **Read the full documentation:** `README.md`
2. **Check the development plan:** `dev-plan.md`
3. **Explore deployment options:** `scripts/deploy_server.md`
4. **Contribute:** See `CONTRIBUTING.md` (if available)

## Getting Help

- **GitHub Issues:** [Create an issue](https://github.com/BRAC/bengali-dialect-transcription/issues)
- **Email:** [TODO: Add support email]
- **Documentation:** Check `README.md` for detailed instructions

---

**Happy transcribing! 🎙️🇧🇩**
