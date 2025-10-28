# Quick Start Guide - Fixed Commands

## ⚠️ Important: Use `python3` instead of `python` on macOS

macOS uses `python3` by default. Always use `python3` in all commands.

## 📥 Step 1: Download Datasets (CORRECTED)

You have **3 options**:

### Option A: Use the Simplified Downloader (Recommended)

```bash
cd /Users/digantohaque/python/BracV1
source venv/bin/activate
python3 data/download_simple.py
```

This will give you a menu to choose which datasets to download.

### Option B: Login to Hugging Face First (For Common Voice)

```bash
# Step 1: Login to Hugging Face
huggingface-cli login
# Paste your token from: https://huggingface.co/settings/tokens

# Step 2: Accept Common Voice terms
# Visit: https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0
# Click "Agree and access repository"

# Step 3: Download
python3 data/download_simple.py
```

### Option C: Create Sample Data for Testing

```bash
python3 data/download_simple.py
# Select option 3 to create sample test data
```

## 🔧 Step 2: Preprocess Data

**After datasets are downloaded**, run:

```bash
python3 data/preprocess.py \
  --input_dirs data/raw/common_voice_bn data/raw/sample_bengali \
  --output_dir data/processed \
  --speaker_split
```

## 🎯 Step 3: Augment Data (Optional)

```bash
python3 data/augment.py \
  --input data/processed/train.tsv \
  --output data/augmented/train_augmented.tsv \
  --speed_perturbation \
  --noise_injection
```

## 🚀 Step 4: Train Model

```bash
python3 train/wav2vec2_finetune.py \
  --train_data data/processed/train.tsv \
  --valid_data data/processed/valid.tsv \
  --output_dir models/wav2vec2_bengali
```

## 📊 Step 5: Evaluate

```bash
python3 eval/eval_wer_cer.py \
  --model_path models/wav2vec2_bengali/checkpoint-best \
  --test_data data/processed/test.tsv \
  --output_dir eval/results
```

## 🌐 Step 6: Run Inference Server

```bash
python3 inference/server.py
```

Then open: http://localhost:8000/docs

## 🆘 Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `command not found: python` | Use `python3` instead |
| `command not found: #` | Don't copy comments, run commands one at a time |
| `ModuleNotFoundError` | Make sure venv is active: `source venv/bin/activate` |
| `404 Not Found` (OpenSLR) | Use the simplified downloader or download manually |
| Hugging Face auth error | Run `huggingface-cli login` first |
| Port 8000 in use | Use different port: `python3 inference/server.py --port 8001` |

## 📝 Summary of Corrected Commands

```bash
# ALWAYS start with this:
cd /Users/digantohaque/python/BracV1
source venv/bin/activate

# Then run ONE command at a time:
python3 data/download_simple.py
python3 data/preprocess.py --input_dirs data/raw/sample_bengali --output_dir data/processed
python3 train/wav2vec2_finetune.py --train_data data/processed/train.tsv --valid_data data/processed/valid.tsv --output_dir models/wav2vec2_bengali
python3 inference/server.py
```

## 💡 Pro Tips

1. **Check if venv is active**: Your prompt should show `(venv)`
2. **Run commands one at a time**: Don't copy entire code blocks
3. **Use Tab completion**: Type `python3 data/dow` then press Tab
4. **Check for errors**: Read error messages carefully
5. **Use the simple downloader**: It handles authentication better

For more help, see: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
