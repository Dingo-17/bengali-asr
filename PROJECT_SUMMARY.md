# 🎯 Bengali Dialect Transcription Project - Complete Repository

## ✅ Repository Structure Created

This Git repository contains a complete, production-ready Bengali dialect transcription system for BRAC with the following structure:

```
BracV1/
├── README.md                           # Comprehensive project documentation
├── dev-plan.md                         # Development milestones (M1-M4)
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore patterns
├── requirements.txt                    # Python dependencies
│
├── data/                               # Data collection and preprocessing
│   ├── download_datasets.py            # Download OpenSLR, Common Voice, Bengali.AI
│   ├── preprocess.py                   # Audio preprocessing pipeline
│   ├── augment.py                      # Data augmentation utilities
│   ├── manifests/                      # Dataset metadata (auto-generated)
│   ├── brac_dialect/                   # BRAC-specific dialect data
│   └── brac_corrections/               # User corrections for active learning
│
├── train/                              # Model training scripts
│   ├── wav2vec2_finetune.py            # Wav2Vec2 fine-tuning
│   ├── whisper_finetune.py             # Whisper fine-tuning
│   ├── utils.py                        # Training utilities (text normalization, etc.)
│   └── finetune_config.yaml            # Training configuration
│
├── eval/                               # Model evaluation
│   └── eval_wer_cer.py                 # WER/CER evaluation with error analysis
│
├── inference/                          # Inference server and deployment
│   ├── server.py                       # FastAPI server with REST endpoints
│   ├── transliterate.py                # Bengali ↔ IPA ↔ Latin transliteration
│   ├── export_model.sh                 # Model export (TorchScript, ONNX, Whisper.cpp)
│   ├── Dockerfile.cpu                  # CPU container
│   ├── Dockerfile.gpu                  # GPU container
│   ├── docker-compose.cpu.yml          # Docker Compose for CPU
│   └── docker-compose.gpu.yml          # Docker Compose for GPU
│
├── frontend/                           # React web interface
│   ├── README.md                       # Frontend documentation
│   ├── package.json                    # NPM dependencies
│   └── src/
│       └── App.jsx                     # Main React component (drag-drop, transcription UI)
│
├── scripts/                            # Deployment scripts
│   ├── deploy_frontend.sh              # Deploy to GitHub Pages
│   └── deploy_server.md                # Server deployment guide (HF, Railway, GCP, AWS)
│
└── notebooks/                          # Analysis notebooks
    └── analysis.ipynb                  # Sample inference and error visualization
```

---

## 🚀 Quick Start Guide

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd BracV1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Datasets

```bash
cd data
python download_datasets.py --datasets all --output ./raw
```

### 3. Preprocess Data

```bash
python preprocess.py \
  --input_dirs ./raw/openslr_slr53 ./raw/common_voice_bn \
  --output_dir ./processed \
  --speaker_split
```

### 4. Train Model

```bash
cd ../train
python wav2vec2_finetune.py \
  --train_data ../data/processed/train.tsv \
  --valid_data ../data/processed/valid.tsv \
  --output_dir ../models/wav2vec2_bengali
```

### 5. Evaluate

```bash
cd ../eval
python eval_wer_cer.py \
  --model_path ../models/wav2vec2_bengali/checkpoint-best \
  --test_data ../data/processed/test.tsv \
  --detailed_analysis
```

### 6. Start Inference Server

```bash
cd ../inference
docker-compose -f docker-compose.cpu.yml up
```

### 7. Deploy Frontend

```bash
cd ../frontend
npm install
npm run dev  # Development
npm run build  # Production build
```

---

## 📋 Key Features Implemented

### ✅ Data Pipeline
- ✓ Automated dataset downloaders (OpenSLR, Common Voice, Bengali.AI)
- ✓ Audio preprocessing (16kHz resampling, normalization, silence trimming)
- ✓ Speaker-level splitting (prevents data leakage)
- ✓ Data augmentation (speed perturbation, noise injection, volume changes)

### ✅ Training Infrastructure
- ✓ Wav2Vec2-XLSR-53 fine-tuning script
- ✓ Whisper fine-tuning script
- ✓ Mixed precision training (FP16)
- ✓ Gradient accumulation and checkpointing
- ✓ W&B logging integration
- ✓ Early stopping
- ✓ Bengali text normalization utilities

### ✅ Evaluation & Analysis
- ✓ WER/CER calculation
- ✓ Per-dialect error breakdown
- ✓ Error pattern analysis (substitutions, deletions, insertions)
- ✓ Number and code-switching error detection
- ✓ Jupyter notebook for interactive analysis

### ✅ Inference & Deployment
- ✓ FastAPI REST API with OpenAPI docs
- ✓ Endpoints: `/transcribe`, `/transcribe/phonetic`, `/health`
- ✓ Rate limiting (10 req/min)
- ✓ Audio format validation
- ✓ Transliteration support (Epitran + Aksharamukha)
- ✓ Confidence-based fallback mechanism
- ✓ Docker containers (CPU and GPU)
- ✓ Model export scripts (TorchScript, ONNX, Whisper.cpp)

### ✅ Frontend
- ✓ React 18+ with Vite
- ✓ Tailwind CSS styling with dark mode
- ✓ Drag & drop file upload
- ✓ Audio player preview
- ✓ Real-time transcription
- ✓ Toggle Bangla/Latin script
- ✓ Download .txt and .srt
- ✓ Responsive design
- ✓ Accessibility (WCAG 2.1)

### ✅ DevOps & Documentation
- ✓ Comprehensive README with decision rationale
- ✓ Development plan with 4 milestones
- ✓ Deployment guides (Hugging Face, Railway, Vercel, GCP, AWS, self-hosted)
- ✓ Frontend deployment script (GitHub Pages)
- ✓ Docker Compose files
- ✓ .gitignore and LICENSE (MIT)

---

## 🎓 Decision Rationale

### Why Fine-tuning Over English-Transliteration?

The repository includes detailed rationale in `README.md` explaining why we chose fine-tuning Bengali ASR models over an English-transliteration shortcut:

1. **Phoneme Loss**: Bengali has unique phonemes not in English
2. **Homophone Confusion**: Multiple spellings for similar sounds
3. **Dialect Variations**: Regional pronunciations don't map to English
4. **Compound Characters**: যুক্তাক্ষর (conjunct consonants) require Bengali understanding
5. **Code-Switching**: Better handling of Bengali-English mixing

**Our Approach:**
- Primary: Fine-tune XLSR-Wav2Vec2 and Whisper on Bengali data
- Fallback: Transliteration only when confidence < 0.7
- Hybrid: Combine acoustic model with domain-specific language model

---

## 🛠️ Technologies Used

**ML/Data:**
- PyTorch, Transformers (Hugging Face)
- Librosa, Soundfile
- Datasets (Hugging Face)
- Epitran, Aksharamukha (transliteration)

**Backend:**
- FastAPI, Uvicorn
- Docker, Docker Compose

**Frontend:**
- React 18, Vite
- Tailwind CSS
- Axios, React Dropzone

**Evaluation:**
- Jiwer (WER/CER)
- Matplotlib, Seaborn (visualization)

---

## 📊 Development Milestones

### M1: Data Collection + Baseline (Weeks 1-2)
- Download datasets
- Preprocess
- Train baseline Wav2Vec2
- Target: WER < 30%

### M2: BRAC Dialect Integration (Weeks 3-6)
- Collect BRAC dialect data
- Fine-tune on combined datasets
- Detailed evaluation
- Target: WER < 20%

### M3: Inference Server + Frontend (Weeks 7-8)
- FastAPI server
- React frontend
- Docker deployment
- GitHub Pages hosting

### M4: Active Learning (Weeks 9-10 + Ongoing)
- Correction submission system
- Automated retraining
- Monitoring dashboard

---

## 🔄 Active Learning Pipeline

The system supports continuous improvement:

1. Users submit corrections via frontend
2. Corrections stored in `data/brac_corrections/`
3. Weekly/monthly automated retraining
4. Model performance tracking

---

## 📚 Datasets & References

**Datasets:**
- OpenSLR SLR53: https://www.openslr.org/53/
- Mozilla Common Voice (bn): https://commonvoice.mozilla.org/bn
- Bengali.AI: https://bengali.ai/

**Transliteration:**
- Epitran: https://github.com/dmort27/epitran
- Aksharamukha: https://github.com/virtualvinodh/aksharamukha

**Papers:**
- Wav2Vec 2.0 (Baevski et al., 2020)
- Whisper (Radford et al., 2022)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and create PR

---

## 📄 License

MIT License - Open source for BRAC and community use.

---

## 🎉 Summary

This repository provides a **complete, production-ready** Bengali dialect transcription system with:

- ✅ End-to-end data pipeline
- ✅ State-of-the-art model training (Wav2Vec2, Whisper)
- ✅ REST API for inference
- ✅ Modern React frontend
- ✅ Multiple deployment options
- ✅ Active learning capabilities
- ✅ Comprehensive documentation

**Ready to deploy and start transcribing!** 🚀

---

*Created: October 29, 2025*  
*Author: BRAC Data Science Team*
