# Deploy to GitHub Pages - Complete Guide

This guide will help you deploy your Bengali ASR system to GitHub Pages (frontend) and Railway.app (backend).

## Prerequisites

- GitHub account
- Railway.app account (free tier: https://railway.app)
- Git installed on your machine
- Code pushed to a GitHub repository

## Part 1: Deploy Backend to Railway.app

### Step 1: Prepare Railway Configuration

The repository already includes `railway.toml` configuration. Make sure it exists:

```toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn inference.server:app --host 0.0.0.0 --port $PORT --workers 2"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Step 2: Deploy to Railway

1. **Sign up/Login to Railway**: Go to https://railway.app
2. **Create New Project**: Click "New Project"
3. **Deploy from GitHub**: 
   - Connect your GitHub account
   - Select your repository
   - Railway will auto-detect Python and deploy
4. **Set Environment Variables** (in Railway dashboard):
   ```
   MODEL_TYPE=wav2vec2
   MODEL_PATH=./models/wav2vec2_bengali/checkpoint-best
   PYTHON_VERSION=3.10
   ```
5. **Get Your API URL**: 
   - Railway will provide a URL like: `https://your-app-name.up.railway.app`
   - Copy this URL (you'll need it for the frontend)

### Step 3: Test Backend

```bash
# Test health endpoint
curl https://your-app-name.up.railway.app/health

# Should return: {"status":"ok","model_loaded":true,...}
```

## Part 2: Deploy Frontend to GitHub Pages

### Step 1: Update API URL

Edit `docs/script.js` and replace localhost with your Railway URL:

```javascript
const API_URL = 'https://your-app-name.up.railway.app';  // Your Railway URL here
```

### Step 2: Commit and Push

```bash
cd /Users/digantohaque/python/BracV1
git add .
git commit -m "Update API URL for production deployment"
git push origin main
```

### Step 3: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Pages** in the left sidebar
4. Under "Source", select:
   - **Branch**: `main`
   - **Folder**: `/docs`
5. Click **Save**
6. GitHub will build and deploy your site
7. Your site will be live at: `https://yourusername.github.io/repository-name/`

### Step 4: Test Production Site

1. Visit your GitHub Pages URL
2. Go to "Try Demo" section
3. Upload an audio file
4. Click "Transcribe"
5. You should see the transcription result

## Part 3: Alternative Backend Deployments

### Option A: Render.com (Free Tier)

1. Create `render.yaml` (already exists):
```yaml
services:
  - type: web
    name: bengali-asr-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn inference.server:app --host 0.0.0.0 --port $PORT"
```

2. Deploy:
   - Go to https://render.com
   - New -> Web Service
   - Connect GitHub repo
   - Render will auto-deploy

### Option B: Heroku (with Procfile)

1. Create Heroku app:
```bash
heroku create your-app-name
git push heroku main
```

2. Set environment variables:
```bash
heroku config:set MODEL_TYPE=wav2vec2
heroku config:set MODEL_PATH=./models/wav2vec2_bengali/checkpoint-best
```

### Option C: Local Development

For testing locally before deploying:

```bash
# Terminal 1: Start backend
cd /Users/digantohaque/python/BracV1
python -m uvicorn inference.server:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend (simple HTTP server)
cd /Users/digantohaque/python/BracV1/docs
python -m http.server 3000

# Visit: http://localhost:3000
```

## Troubleshooting

### Issue: CORS errors

**Solution**: Backend already has CORS enabled. If you still see errors, check:

```python
# In inference/server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Model not loading on Railway

**Solution**: Railway free tier has limited memory. Use a smaller model or upgrade.

1. Add to `railway.toml`:
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
```

2. Or use CPU-only lightweight model

### Issue: GitHub Pages not updating

**Solution**: 
- Clear browser cache
- Wait 2-3 minutes for GitHub to rebuild
- Check GitHub Actions tab for build status
- Make sure `/docs` folder is selected in settings

### Issue: Audio upload fails

**Solution**:
- Check file size (max 10MB by default)
- Check file format (supported: wav, mp3, ogg, flac, m4a)
- Check browser console for detailed errors

## Production Checklist

- [ ] Backend deployed and health check passes
- [ ] API URL updated in frontend
- [ ] Frontend deployed to GitHub Pages
- [ ] End-to-end test: upload audio and get transcription
- [ ] Check mobile responsiveness
- [ ] Set up custom domain (optional)
- [ ] Configure analytics (optional)
- [ ] Set up error monitoring (optional)

## Custom Domain (Optional)

### For Frontend (GitHub Pages):

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. Add CNAME record pointing to: `yourusername.github.io`
3. Create `docs/CNAME` file with your domain:
```
bengali-asr.yourdomain.com
```
4. Update GitHub Pages settings to use custom domain

### For Backend (Railway):

1. In Railway dashboard, go to Settings
2. Under "Domains", click "Generate Domain" or add custom domain
3. Update DNS records as instructed

## Next Steps

1. **Monitor Performance**: Check Railway/Render logs for errors
2. **Optimize Model**: Use quantization or distillation for faster inference
3. **Add Features**: 
   - Real-time transcription with WebSocket
   - Multi-language support
   - Speaker diarization
4. **Analytics**: Add Google Analytics or Plausible
5. **SEO**: Add meta tags, sitemap, robots.txt
6. **Security**: Add rate limiting, authentication for API

## Support

For issues, check:
- GitHub Issues: [Your Repo URL]
- Railway Docs: https://docs.railway.app
- GitHub Pages Docs: https://docs.github.com/pages

---

**Your deployment is ready! 🚀**

Frontend: `https://yourusername.github.io/repository-name/`
Backend: `https://your-app-name.up.railway.app/`
