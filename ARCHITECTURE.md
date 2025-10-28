# 🏗️ System Architecture & Deployment

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│                    (Chrome, Safari, Firefox)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GITHUB PAGES (CDN)                         │
│                   https://username.github.io                    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  index.html  │  │  styles.css  │  │  script.js   │        │
│  │              │  │              │  │              │        │
│  │ Landing Page │  │ Responsive   │  │ API Client   │        │
│  │ UI Components│  │ Design       │  │ File Upload  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls (fetch)
                             │ POST /transcribe
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAILWAY.APP / RENDER.COM                     │
│                  https://your-app.up.railway.app                │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    FastAPI Server                         │ │
│  │                  (inference/server.py)                    │ │
│  │                                                           │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│  │  │  /health │  │/transcribe│  │  /docs   │              │ │
│  │  └──────────┘  └──────────┘  └──────────┘              │ │
│  │                                                           │ │
│  │  Endpoints:                                               │ │
│  │  • Health Check                                           │ │
│  │  • Audio Transcription                                    │ │
│  │  • Phonetic Conversion                                    │ │
│  │  • API Documentation                                      │ │
│  └───────────────────────┬───────────────────────────────────┘ │
│                          │                                     │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   ML Models                               │ │
│  │                                                           │ │
│  │  ┌──────────────────┐      ┌──────────────────┐         │ │
│  │  │   Wav2Vec2       │      │   Whisper        │         │ │
│  │  │   (Facebook)     │      │   (OpenAI)       │         │ │
│  │  │                  │      │                  │         │ │
│  │  │ Bengali ASR      │      │ Multilingual     │         │ │
│  │  │ Fine-tuned       │      │ Fine-tuned       │         │ │
│  │  └──────────────────┘      └──────────────────┘         │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow

```
1. User Action
   │
   ├─> User uploads audio file (WAV/MP3/etc.)
   │
   └─> Clicks "Transcribe" button
        │
        ▼
        
2. Frontend Processing
   │
   ├─> JavaScript validates file
   │   • Check file type
   │   • Check file size
   │   • Show loading state
   │
   └─> Creates FormData with audio
        │
        ▼
        
3. API Request
   │
   └─> POST https://your-app.up.railway.app/transcribe
       │
       │ Headers:
       │  • Content-Type: multipart/form-data
       │  • Origin: https://username.github.io
       │
       │ Body:
       │  • file: [audio binary data]
       │
       ▼
       
4. Backend Processing
   │
   ├─> CORS validation (allows GitHub Pages origin)
   │
   ├─> File validation
   │   • Check file extension
   │   • Check file size (<10MB)
   │   • Check audio duration (<60s)
   │
   ├─> Audio preprocessing
   │   • Load with librosa
   │   • Resample to 16kHz
   │   • Convert to mono
   │
   ├─> Model inference
   │   • Load Wav2Vec2/Whisper model
   │   • Process audio through model
   │   • Get logits and predictions
   │
   └─> Post-processing
       • Decode tokens to text
       • Calculate confidence score
       • Optional: Transliterate to Latin
        │
        ▼
        
5. API Response
   │
   └─> Returns JSON:
       {
         "transcript_bangla": "বাংলা টেক্সট",
         "confidence": 0.95,
         "tokens": [...],
         "processing_time_ms": 1234
       }
        │
        ▼
        
6. Frontend Display
   │
   ├─> Hide loading state
   │
   ├─> Display transcription
   │   • Show Bengali text
   │   • Show confidence score
   │   • Show processing time
   │
   └─> Enable actions
       • Copy to clipboard
       • Download as text
       • Transcribe another file
```

## 🌐 Deployment Architecture

### Development Environment
```
┌──────────────────────────────────────┐
│      Local Development (macOS)       │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Terminal 1: Backend           │ │
│  │  $ uvicorn server:app          │ │
│  │  → http://localhost:8000       │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Terminal 2: Frontend          │ │
│  │  $ python -m http.server 3000  │ │
│  │  → http://localhost:3000       │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

### Production Environment
```
┌───────────────────────────────────────────────────────────┐
│                    PRODUCTION STACK                       │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              GitHub (Source Control)                │ │
│  │         https://github.com/user/repo                │ │
│  │                                                     │ │
│  │  • Version control                                  │ │
│  │  • CI/CD trigger                                    │ │
│  │  • Collaboration                                    │ │
│  └──────────────┬────────────────┬────────────────────┘ │
│                 │                │                       │
│                 │                │                       │
│       ┌─────────▼────────┐  ┌───▼──────────────┐       │
│       │  GitHub Pages    │  │   Railway.app    │       │
│       │   (Frontend)     │  │   (Backend)      │       │
│       │                  │  │                  │       │
│       │ Static Files     │  │ FastAPI Server   │       │
│       │ • HTML/CSS/JS    │  │ • ML Models      │       │
│       │ • Auto Deploy    │  │ • Auto Deploy    │       │
│       │ • CDN            │  │ • Auto Scale     │       │
│       │ • HTTPS          │  │ • HTTPS          │       │
│       └──────────────────┘  └──────────────────┘       │
└───────────────────────────────────────────────────────────┘
```

## 📦 Technology Stack

### Frontend Stack
```
┌─────────────────────────────┐
│       Static Website        │
├─────────────────────────────┤
│ • HTML5                     │
│ • CSS3 (Custom Variables)   │
│ • Vanilla JavaScript (ES6+) │
│ • Fetch API                 │
│ • FormData API              │
│ • File API                  │
└─────────────────────────────┘

Dependencies: None (Pure vanilla!)
Hosting: GitHub Pages (Free)
CDN: GitHub's CDN
SSL: Automatic
```

### Backend Stack
```
┌─────────────────────────────┐
│      Python Backend         │
├─────────────────────────────┤
│ • Python 3.10+              │
│ • FastAPI (Web Framework)   │
│ • Uvicorn (ASGI Server)     │
│ • PyTorch (ML Framework)    │
│ • Transformers (Models)     │
│ • Librosa (Audio Processing)│
│ • Slowapi (Rate Limiting)   │
└─────────────────────────────┘

Hosting: Railway.app / Render.com
Container: Docker (optional)
Scaling: Horizontal (auto)
```

### ML Model Stack
```
┌─────────────────────────────┐
│      ML Models              │
├─────────────────────────────┤
│ • Wav2Vec2 (Facebook)       │
│   - Bengali fine-tuned      │
│   - ~300M parameters        │
│                             │
│ • Whisper (OpenAI)          │
│   - Multilingual            │
│   - ~244M params (base)     │
└─────────────────────────────┘

Framework: HuggingFace Transformers
Optimization: CPU inference (free tier)
Future: GPU for faster processing
```

## 🔐 Security Architecture

```
┌────────────────────────────────────────────┐
│           Security Layers                  │
├────────────────────────────────────────────┤
│                                            │
│  1. Transport Security                     │
│     ✓ HTTPS only (TLS 1.2+)               │
│     ✓ Automatic SSL certificates          │
│                                            │
│  2. CORS Protection                        │
│     ✓ Configured origins                  │
│     ✓ Credential handling                 │
│     ✓ Method restrictions                 │
│                                            │
│  3. Rate Limiting                          │
│     ✓ 10 requests/minute per IP           │
│     ✓ Prevents abuse                      │
│     ✓ Configurable limits                 │
│                                            │
│  4. Input Validation                       │
│     ✓ File type checking                  │
│     ✓ File size limits (10MB)             │
│     ✓ Audio duration limits (60s)         │
│     ✓ Malformed file rejection            │
│                                            │
│  5. Error Handling                         │
│     ✓ No sensitive data in errors         │
│     ✓ Sanitized error messages            │
│     ✓ Logging for monitoring              │
└────────────────────────────────────────────┘
```

## 📈 Scalability

### Current Setup (Free Tier)
```
GitHub Pages:
├─ Bandwidth: 100 GB/month
├─ Concurrent Users: Unlimited (CDN)
└─ Builds: 10 per hour

Railway (Free):
├─ Credit: $5/month (~500 hours)
├─ RAM: 512 MB
├─ CPU: Shared
├─ Requests: ~10-50 concurrent
└─ Cold starts: ~5-10 seconds
```

### Scaling Up
```
┌─────────────────────────────────────────┐
│          Scaling Strategy               │
├─────────────────────────────────────────┤
│                                         │
│  Load → Action                          │
│                                         │
│  100 users/day                          │
│  ↓                                      │
│  Free tier (current)                    │
│                                         │
│  1,000 users/day                        │
│  ↓                                      │
│  Railway Pro ($5-20/month)              │
│  • More RAM (1-2 GB)                    │
│  • Faster CPU                           │
│                                         │
│  10,000 users/day                       │
│  ↓                                      │
│  Dedicated Server + GPU                 │
│  • AWS/GCP/Azure                        │
│  • GPU for inference                    │
│  • Load balancing                       │
│  • Auto-scaling                         │
│                                         │
│  100,000+ users/day                     │
│  ↓                                      │
│  Microservices Architecture             │
│  • Separate inference service           │
│  • Message queue (Redis/RabbitMQ)       │
│  • Multiple replicas                    │
│  • CDN for static assets                │
│  • Database for analytics               │
└─────────────────────────────────────────┘
```

## 🔄 CI/CD Pipeline

```
┌────────────────────────────────────────────────┐
│            Continuous Deployment               │
└────────────────────────────────────────────────┘

Developer
    │
    │ git add . && git commit -m "Update"
    │ git push origin main
    ▼
┌──────────────────┐
│  GitHub          │
│  (main branch)   │
└────┬────────┬────┘
     │        │
     │        │ Webhook triggers
     │        │
     ▼        ▼
┌─────────┐ ┌──────────┐
│ GitHub  │ │ Railway  │
│ Pages   │ │ App      │
│         │ │          │
│ Build   │ │ Build    │
│ ↓       │ │ ↓        │
│ Deploy  │ │ Deploy   │
│ ↓       │ │ ↓        │
│ Live    │ │ Live     │
└─────────┘ └──────────┘
    │            │
    │            │
    ▼            ▼
  Frontend     Backend
   Live         Live
```

## 🗺️ Data Flow

```
Audio File Journey:

1. User's Device
   └─> [audio.wav] - Original file
        │
        ▼
        
2. Browser (JavaScript)
   └─> [File object] - Selected via input
        │
        │ Validation
        │ • Type check
        │ • Size check
        ▼
        
3. FormData API
   └─> [multipart/form-data] - Prepared for upload
        │
        │ fetch() API
        │ HTTPS
        ▼
        
4. FastAPI Server
   └─> [UploadFile] - Received in endpoint
        │
        │ Temporary storage
        ▼
        
5. Audio Processing (librosa)
   └─> [numpy array] - Audio signal
        │
        │ Resample: 16kHz
        │ Convert: mono
        ▼
        
6. ML Model (Wav2Vec2/Whisper)
   └─> [logits] - Model predictions
        │
        │ Decode
        ▼
        
7. Post-processing
   └─> [text string] - Bengali transcription
        │
        │ JSON serialization
        ▼
        
8. API Response
   └─> [JSON] - Structured response
        │
        │ HTTPS
        ▼
        
9. Browser (JavaScript)
   └─> [JavaScript object] - Parsed JSON
        │
        │ Display
        ▼
        
10. User's Screen
    └─> Bengali transcription text
```

## 📊 Monitoring & Analytics

```
Observability Stack:

┌─────────────────────────────────────────┐
│            Production Monitoring         │
├─────────────────────────────────────────┤
│                                         │
│  Frontend (GitHub Pages)                │
│  └─> Built-in analytics                 │
│      └─> Traffic metrics                │
│                                         │
│  Backend (Railway)                      │
│  ├─> Application logs                   │
│  ├─> Performance metrics                │
│  ├─> Error tracking                     │
│  └─> Resource usage                     │
│                                         │
│  Optional Add-ons:                      │
│  ├─> Google Analytics (frontend)        │
│  ├─> Sentry (error tracking)            │
│  ├─> Datadog (full stack)               │
│  └─> Custom logging                     │
└─────────────────────────────────────────┘
```

---

**This architecture supports:**
- ✅ Serverless deployment (free tier)
- ✅ Auto-scaling
- ✅ Global CDN
- ✅ HTTPS by default
- ✅ Easy updates (git push)
- ✅ Production-ready security
