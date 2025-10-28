# Bengali Dialect Transcription System for BRAC

A production-ready Automatic Speech Recognition (ASR) system for Bengali dialects, fine-tuned on multiple datasets and optimized for BRAC's regional dialect variations.

## 🚀 **NEW: Quick Deployment**

**Get your system live in 15 minutes!**

```bash
# One-command deployment
./start.sh
```

**Or follow the guides:**
- 📘 **Beginners**: [GETTING_STARTED.md](./GETTING_STARTED.md) - Step-by-step deployment (20 min)
- ⚡ **Fast Track**: [QUICKSTART_DEPLOY.md](./QUICKSTART_DEPLOY.md) - Quick deployment (15 min)
- 📚 **All Docs**: [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) - Complete documentation index

**Demo**: See your deployed system at:
- Frontend: `https://YOUR_USERNAME.github.io/bengali-asr/`
- Backend: `https://your-app.up.railway.app`

---

## 📋 Project Overview

This system provides end-to-end Bengali speech-to-text transcription with support for:
- Multiple Bengali dialects and regional variations
- High-accuracy transcription using state-of-the-art models (Wav2Vec2, Whisper)
- Phonetic transliteration (Bengali ↔ IPA ↔ Latin)
- REST API for integration
- Modern React frontend with real-time transcription
- Active learning pipeline for continuous improvement

## 🗂️ Datasets

### Primary Datasets

1. **OpenSLR SLR53** - Bengali ASR training data corpus
   - Link: https://www.openslr.org/53/
   - ~196 hours of read Bengali speech
   - Citation: _"Bengali ASR training data corpus", OpenSLR, 2018_

2. **Mozilla Common Voice (bn)**
   - Link: https://commonvoice.mozilla.org/bn
   - Community-contributed Bengali speech
   - Citation: _Ardila, R., et al. "Common Voice: A Massively-Multilingual Speech Corpus." LREC 2020_

3. **Bengali.AI Speech Recognition Dataset**
   - Link: https://huggingface.co/datasets/BengaliAI/bengali_speech
   - Diverse Bengali dialects
   - Citation: [To be added based on dataset version]

### BRAC Dialect Dataset (Custom)
- Regional dialect variations from BRAC's operational areas
- Format: CSV with columns `filepath,transcript,region,speaker_id`
- Location: `data/brac_dialect/`

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+
python --version

# GPU recommended (CUDA 11.7+) but CPU works for inference
nvidia-smi  # Check GPU availability
```

### Installation
```bash
# Clone repository
git clone https://github.com/BRAC/bengali-dialect-transcription.git
cd bengali-dialect-transcription

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install additional tools for transliteration
pip install epitran aksharamukha
```

## 📊 End-to-End Pipeline

### 1. Data Download
```bash
# Download and prepare datasets
cd data
python download_datasets.py --datasets openslr common_voice bengaliai --output ./raw

# This will create:
# data/raw/openslr_slr53/
# data/raw/common_voice_bn/
# data/raw/bengaliai/
# data/manifests/  (dataset metadata)
```

### 2. Data Preprocessing
```bash
# Preprocess and create train/valid/test splits
python preprocess.py \
  --input_dirs ./raw/openslr_slr53 ./raw/common_voice_bn ./raw/bengaliai \
  --output_dir ./processed \
  --sample_rate 16000 \
  --speaker_split  # Ensures no speaker leakage

# Output: data/processed/{train,valid,test}.tsv
# Format: path\ttranscript\tspeaker\tlocale
```

### 3. Data Augmentation (Optional)
```bash
# Apply augmentation to training data
python augment.py \
  --input data/processed/train.tsv \
  --output data/augmented/train_augmented.tsv \
  --speed_perturbation \
  --noise_injection \
  --volume_augmentation
```

### 4. Model Training

#### Option A: Fine-tune Wav2Vec2
```bash
cd train
python wav2vec2_finetune.py \
  --config finetune_config.yaml \
  --model_name facebook/wav2vec2-large-xlsr-53 \
  --output_dir ../models/wav2vec2_bengali \
  --train_data ../data/processed/train.tsv \
  --valid_data ../data/processed/valid.tsv \
  --mixed_precision \
  --wandb_logging  # Optional: requires WANDB_API_KEY
```

#### Option B: Fine-tune Whisper
```bash
python whisper_finetune.py \
  --config finetune_config.yaml \
  --model_name openai/whisper-small \
  --output_dir ../models/whisper_bengali \
  --train_data ../data/processed/train.tsv \
  --valid_data ../data/processed/valid.tsv \
  --early_stopping
```

#### Adding BRAC Dialect Data (Continued Fine-tuning)
```bash
# After initial training, continue with BRAC dialect data
python wav2vec2_finetune.py \
  --config finetune_config.yaml \
  --model_name ../models/wav2vec2_bengali/checkpoint-best \
  --output_dir ../models/wav2vec2_brac_dialect \
  --train_data ../data/brac_dialect/train.tsv \
  --valid_data ../data/brac_dialect/valid.tsv \
  --learning_rate 1e-5  # Lower LR for fine-tuning
```

### 5. Evaluation
```bash
cd eval
python eval_wer_cer.py \
  --model_path ../models/wav2vec2_brac_dialect/checkpoint-best \
  --test_data ../data/processed/test.tsv \
  --output_dir ./results \
  --detailed_analysis  # Includes confusion breakdown
```

### 6. Model Export
```bash
cd inference
bash export_model.sh \
  --model_path ../models/wav2vec2_brac_dialect/checkpoint-best \
  --output_format torchscript onnx \
  --quantize  # Optional: for deployment optimization
```

### 7. Inference Server
```bash
cd inference

# CPU deployment
docker-compose -f docker-compose.cpu.yml up

# GPU deployment
docker-compose -f docker-compose.gpu.yml up

# Server will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 8. Frontend Deployment
```bash
cd frontend
npm install
npm run build

# Deploy to GitHub Pages
bash ../scripts/deploy_frontend.sh
```

## 🔌 API Usage

### Transcribe Audio
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio=@sample.wav" \
  -F "language=bn"
```

Response:
```json
{
  "transcript_bangla": "আমি বাংলায় কথা বলছি",
  "transcript_latin": "ami banglay kotha bolchi",
  "confidence": 0.95,
  "tokens": ["আমি", "বাংলায়", "কথা", "বলছি"]
}
```

### Phonetic Transcription
```bash
curl -X POST "http://localhost:8000/transcribe/phonetic" \
  -F "audio=@sample.wav" \
  -F "output_format=ipa"
```

## 🎨 Frontend Features

- **Drag & Drop**: Upload audio files easily
- **Real-time Preview**: Play audio before transcription
- **Multiple Formats**: View in Bangla script or Latin phonetic
- **Export Options**: Download as .txt or .srt
- **Responsive Design**: Works on desktop and mobile
- **Accessibility**: WCAG 2.1 compliant

Access demo: [https://brac.github.io/bengali-dialect-transcription](https://brac.github.io/bengali-dialect-transcription)

## 🔄 Active Learning Loop

The system supports continuous improvement through user corrections:

1. Users submit corrections via the frontend
2. Corrections stored in `data/brac_corrections/`
3. Periodic retraining scheduled (weekly/monthly)
4. Model performance tracking over time

## 📁 Repository Structure

```
.
├── README.md                    # This file
├── dev-plan.md                  # Development milestones
├── LICENSE                      # MIT License
├── .gitignore
├── requirements.txt
├── data/
│   ├── download_datasets.py     # Dataset downloader
│   ├── preprocess.py            # Preprocessing pipeline
│   ├── augment.py               # Data augmentation
│   ├── manifests/               # Dataset metadata
│   ├── brac_dialect/            # BRAC-specific data
│   └── brac_corrections/        # User corrections
├── train/
│   ├── wav2vec2_finetune.py     # Wav2Vec2 training
│   ├── whisper_finetune.py      # Whisper training
│   ├── utils.py                 # Training utilities
│   └── finetune_config.yaml     # Training configuration
├── eval/
│   └── eval_wer_cer.py          # Evaluation metrics
├── inference/
│   ├── server.py                # FastAPI server
│   ├── transliterate.py         # Transliteration pipeline
│   ├── export_model.sh          # Model export script
│   ├── Dockerfile.cpu           # CPU container
│   ├── Dockerfile.gpu           # GPU container
│   ├── docker-compose.cpu.yml
│   └── docker-compose.gpu.yml
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── public/
│   └── src/
├── scripts/
│   ├── deploy_frontend.sh       # Frontend deployment
│   └── deploy_server.md         # Server deployment guide
├── notebooks/
│   └── analysis.ipynb           # Sample analysis
└── models/                      # Trained models (gitignored)
```

## 🧠 Decision Rationale

### Why Fine-tuning Over English-Transliteration Shortcut?

**The Problem with Transliteration-Only:**
While it might seem tempting to transcribe Bengali audio to English phonetics and then transliterate back to Bengali script, this approach has critical flaws:

1. **Phoneme Loss**: Bengali has unique phonemes (ড়, ঢ়, ৎ, ং, ঃ) not present in English. Forcing through English loses these distinctions.

2. **Homophone Confusion**: Multiple Bengali words sound similar but have different spellings (e.g., কথা/কথো, দেশ/দ্যাশ). English-based systems can't disambiguate these.

3. **Dialect Variations**: Bengali regional dialects (Sylheti, Chittagonian, Noakhali) have pronunciation patterns that don't map cleanly to standard English phonetics.

4. **Compound Characters**: Bengali script uses যুক্তাক্ষর (conjunct consonants) like ক্ষ, জ্ঞ, ত্র which require understanding of Bengali orthographic rules, not just phonetics.

5. **Code-Switching**: BRAC's operational context involves code-switching between Bengali and English. A Bengali-native model handles this better.

**Our Approach:**
- **Primary**: Fine-tune XLSR-Wav2Vec2 and Whisper models directly on Bengali data
- **Fallback**: Use transliteration (Epitran → IPA → Aksharamukha) only when primary model confidence < 0.7
- **Hybrid**: For low-resource dialects, combine acoustic model with language model (KenLM) trained on BRAC's domain-specific text corpus

### Transliteration Tools

1. **Epitran**: G2P (Grapheme-to-Phoneme) conversion
   - Link: https://github.com/dmort27/epitran
   - Converts Bengali script → IPA (International Phonetic Alphabet)

2. **Aksharamukha**: Script conversion library
   - Link: https://github.com/virtualvinodh/aksharamukha
   - Converts between Indic scripts, IPA, and Latin transliteration
   - Useful for: IPA → Bengali, Latin → Bengali

3. **Use Case**: When ASR outputs phonetic tokens with low confidence, transliterate to generate multiple Bengali orthography candidates, then rank by language model probability.

## 📚 References

- Baevski, A., et al. (2020). "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations." NeurIPS 2020.
- Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision." arXiv:2212.04356.
- Bengali.AI: https://bengali.ai/
- Hugging Face Transformers: https://huggingface.co/docs/transformers/

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Authors

- BRAC Data Science Team
- Contact: datasci@brac.net

## 🙏 Acknowledgments

- OpenSLR, Mozilla Common Voice, and Bengali.AI for providing datasets
- Hugging Face for transformer models and infrastructure
- BRAC field teams for dialect data collection

---

**Last Updated**: October 2025
