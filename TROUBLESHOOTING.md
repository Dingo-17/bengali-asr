# Troubleshooting Guide

## Common Issues and Solutions

### 1. ❌ `zsh: command not found: python`

**Problem**: macOS uses `python3` instead of `python` by default.

**Solution**: Always use `python3` instead of `python`:
```bash
# ✗ Wrong
python data/download_datasets.py

# ✓ Correct
python3 data/download_datasets.py
```

**Permanent Fix**: Create an alias in your `~/.zshrc`:
```bash
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

---

### 2. ❌ `zsh: unknown file attribute: h` or `zsh: command not found: #`

**Problem**: Copying multi-line commands with comments (`#`) confuses the shell.

**Solution**: Run commands **one at a time**, without the comments:
```bash
# ✗ Wrong - Don't copy this entire block
python3 data/download_datasets.py
# This is a comment
python3 data/preprocess.py

# ✓ Correct - Run each command separately
python3 data/download_datasets.py
# Then run:
python3 data/preprocess.py
```

---

### 3. ❌ Virtual Environment Not Active

**Problem**: Commands fail because the virtual environment isn't activated.

**Solution**: 
```bash
# Activate the virtual environment
cd /Users/digantohaque/python/BracV1
source venv/bin/activate

# You should see (venv) in your prompt:
# (venv) digantohaque@Wasims-Mac-mini BracV1 %
```

---

### 4. ❌ Dataset Download Errors (404 Not Found)

**Problem**: OpenSLR URLs may have changed or require manual download.

**Solution A - Manual Download**:
1. Visit https://www.openslr.org/53/
2. Download the files manually
3. Extract them to `data/raw/openslr_slr53/`

**Solution B - Use Only Hugging Face Datasets**:
```bash
python3 data/download_datasets.py --datasets common_voice bengaliai --output data/raw
```

---

### 5. ❌ Hugging Face Authentication Required

**Problem**: `GatedRepoError` or authentication errors when downloading Common Voice.

**Solution**:
```bash
# Install Hugging Face CLI (already included in requirements.txt)
# Login with your Hugging Face token
huggingface-cli login

# Get your token from: https://huggingface.co/settings/tokens
# Accept the dataset terms at:
# https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0
```

---

### 6. ❌ FFmpeg Not Found

**Problem**: Audio processing may fail without FFmpeg.

**Solution**:
```bash
# Install FFmpeg using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

---

### 7. ❌ Port 8000 Already in Use

**Problem**: Cannot start inference server because port is in use.

**Solution**:
```bash
# Find the process using port 8000
lsof -ti:8000

# Kill the process (replace PID with the number from above)
kill -9 <PID>

# Or use a different port
python3 inference/server.py --port 8001
```

---

### 8. ❌ CUDA Not Available / GPU Not Detected

**Problem**: macOS doesn't support NVIDIA CUDA.

**Solution**: This is expected on macOS. The system will use:
- **CPU mode** for training and inference (slower but works)
- **MPS (Metal Performance Shaders)** if available (Apple Silicon GPUs)

To check MPS availability:
```python
import torch
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")
```

---

### 9. ❌ Out of Memory Errors

**Problem**: Training fails with OOM errors.

**Solution**:
```bash
# Reduce batch size in training config
# Edit: train/finetune_config.yaml

training:
  batch_size: 4  # Reduce from 16 to 4
  gradient_accumulation_steps: 4  # Increase to maintain effective batch size
```

---

### 10. ❌ Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'xyz'`

**Solution**:
```bash
# Make sure virtual environment is active
source venv/bin/activate

# Reinstall dependencies
pip3 install -r requirements.txt

# Or install specific missing package
pip3 install <package-name>
```

---

## Quick Command Reference

### Activate Virtual Environment
```bash
cd /Users/digantohaque/python/BracV1
source venv/bin/activate
```

### Download Datasets (One at a Time)
```bash
python3 data/download_datasets.py --datasets common_voice --output data/raw
python3 data/download_datasets.py --datasets bengaliai --output data/raw
```

### Preprocess Data
```bash
python3 data/preprocess.py \
  --input_dirs data/raw/common_voice_bn data/raw/bengaliai \
  --output_dir data/processed \
  --speaker_split
```

### Train Model (CPU/MPS)
```bash
python3 train/wav2vec2_finetune.py \
  --train_data data/processed/train.tsv \
  --valid_data data/processed/valid.tsv \
  --output_dir models/wav2vec2_bengali
```

### Run Inference Server
```bash
python3 inference/server.py
```

---

## Getting Help

1. **Check logs**: Most scripts save logs to `logs/` directory
2. **Enable debug mode**: Add `--debug` flag to commands
3. **Read error messages carefully**: They often contain the solution
4. **Check Python version**: Run `python3 --version` (should be 3.8+)
5. **Verify virtual environment**: Look for `(venv)` in your terminal prompt

---

## Contact

For BRAC-specific issues, contact: datasci@brac.net
