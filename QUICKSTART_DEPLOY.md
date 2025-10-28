# 🚀 Quick Deployment Guide

Get your Bengali ASR system live in **15 minutes**!

## 📋 What You'll Deploy

- **Frontend**: Static website on GitHub Pages (FREE)
- **Backend**: FastAPI server on Railway.app or Render.com (FREE)

---

## ⚡ Option 1: Automated Deployment (Recommended)

### Step 1: Run Deployment Script

```bash
cd /Users/digantohaque/python/BracV1
./deploy-github-pages.sh
```

The script will:
- ✅ Initialize git repository (if needed)
- ✅ Update API URL in frontend
- ✅ Commit and push to GitHub
- ✅ Provide step-by-step instructions

### Step 2: Follow On-Screen Instructions

The script will guide you through:
1. Choosing backend deployment platform
2. Setting up GitHub Pages
3. Deploying backend
4. Testing your system

---

## ⚡ Option 2: Manual Deployment

### Part A: Deploy Backend (Choose One)

#### A1. Railway.app (Easiest - Recommended)

1. **Sign Up**: Go to https://railway.app and sign in with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and deploy

3. **Get Your API URL**:
   - After deployment, Railway provides a URL like:
   - `https://your-app-name.up.railway.app`
   - Copy this URL

4. **Test Backend**:
   ```bash
   curl https://your-app-name.up.railway.app/health
   ```
   Should return: `{"status":"ok",...}`

#### A2. Render.com (Alternative)

1. **Sign Up**: https://render.com (sign in with GitHub)

2. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - Name: `bengali-asr-api`
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn inference.server:app --host 0.0.0.0 --port $PORT`

3. **Deploy**: Click "Create Web Service"

4. **Get URL**: `https://bengali-asr-api.onrender.com`

### Part B: Update Frontend

1. **Edit `docs/script.js`**:
   ```javascript
   // Change line 2 from:
   const API_URL = 'http://localhost:8000';
   
   // To:
   const API_URL = 'https://your-app-name.up.railway.app';  // Your Railway URL
   ```

2. **Save the file**

### Part C: Deploy Frontend to GitHub Pages

1. **Initialize Git** (if not done):
   ```bash
   cd /Users/digantohaque/python/BracV1
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `bengali-asr`)
   - Copy the repository URL

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/bengali-asr.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source":
     - Branch: `main`
     - Folder: `/docs`
   - Click **Save**

5. **Wait 2-3 Minutes**: GitHub will build and deploy

6. **Your Site is Live**:
   - URL: `https://YOUR_USERNAME.github.io/bengali-asr/`

---

## ✅ Testing Your Deployment

### Test 1: Backend Health Check

```bash
curl https://your-app-name.up.railway.app/health
```

Expected response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_type": "wav2vec2",
  "device": "cpu"
}
```

### Test 2: Frontend

1. Visit: `https://YOUR_USERNAME.github.io/bengali-asr/`
2. Navigate to "Try Demo" section
3. Upload an audio file (wav, mp3, etc.)
4. Click "Transcribe"
5. Verify transcription appears

### Test 3: API Direct Test

```bash
# Download a sample Bengali audio file or use your own
curl -X POST https://your-app-name.up.railway.app/transcribe \
  -F "file=@path/to/your/audio.wav"
```

---

## 🎯 URLs Cheat Sheet

Fill in your URLs:

```
Frontend (GitHub Pages):
https://[YOUR_USERNAME].github.io/[REPO_NAME]/

Backend (Railway):
https://[YOUR_APP_NAME].up.railway.app

Backend Health Check:
https://[YOUR_APP_NAME].up.railway.app/health

Backend API Docs:
https://[YOUR_APP_NAME].up.railway.app/docs
```

---

## 🔧 Troubleshooting

### Issue: "CORS Error"

**Solution**: Check that backend has CORS enabled (already configured in `inference/server.py`):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: GitHub Pages Shows 404

**Solutions**:
1. Wait 2-3 minutes for GitHub to build
2. Clear browser cache
3. Check that `/docs` folder is selected in Settings → Pages
4. Verify files exist in `/docs` folder

### Issue: Backend Deployment Fails

**Solutions**:

**Railway**:
- Check build logs in Railway dashboard
- Ensure `requirements.txt` exists
- Check memory usage (free tier has limits)

**Render**:
- Check build logs
- Ensure Python version is 3.10
- Verify start command is correct

### Issue: Audio Upload Fails

**Solutions**:
1. Check file format (supported: wav, mp3, ogg, flac, m4a)
2. Check file size (max 10MB)
3. Check browser console for errors (F12)
4. Verify backend is running: `curl [BACKEND_URL]/health`

### Issue: Transcription Takes Too Long

**Causes**:
- Cold start (free tier platforms sleep after inactivity)
- Large audio file
- CPU-only inference

**Solutions**:
- Keep backend "warm" by pinging health endpoint
- Use shorter audio clips for testing
- Upgrade to paid tier for faster CPU/GPU

---

## 🎨 Customization

### Change Frontend Colors

Edit `docs/styles.css`:

```css
:root {
    --primary-color: #YOUR_COLOR;
    --secondary-color: #YOUR_COLOR;
}
```

### Add Custom Domain

**Frontend (GitHub Pages)**:
1. Buy domain
2. Add CNAME record: `YOUR_USERNAME.github.io`
3. Create `docs/CNAME` file with your domain
4. Update GitHub Pages settings

**Backend (Railway)**:
1. Railway Settings → Domains
2. Add custom domain
3. Update DNS records

---

## 📊 Next Steps

Once deployed:

1. **Monitor**: Check Railway/Render logs for errors
2. **Optimize**: 
   - Use quantized models for faster inference
   - Add caching for repeated requests
3. **Enhance**:
   - Add user authentication
   - Support real-time transcription (WebSocket)
   - Multi-language support
4. **Analytics**: Add Google Analytics to track usage
5. **SEO**: Add meta tags, sitemap

---

## 🆘 Need Help?

1. **Check Logs**: 
   - Railway: Dashboard → Deployments → Logs
   - Render: Dashboard → Logs
   - GitHub Pages: Settings → Pages

2. **Documentation**:
   - `DEPLOY_GITHUB_PAGES.md` - Detailed deployment guide
   - `TROUBLESHOOTING.md` - Common issues
   - `README.md` - Project overview

3. **Test Locally First**:
   ```bash
   # Terminal 1: Backend
   uvicorn inference.server:app --reload
   
   # Terminal 2: Frontend
   cd docs && python -m http.server 3000
   ```

---

## ✨ Success Checklist

- [ ] Backend deployed and health check passes
- [ ] Frontend deployed to GitHub Pages
- [ ] API URL updated in `docs/script.js`
- [ ] Can upload audio and get transcription
- [ ] No CORS errors in browser console
- [ ] Mobile-friendly design works
- [ ] Shared site URL with friends/colleagues

---

**Congratulations! Your Bengali ASR system is now live! 🎉**

Share your site: `https://YOUR_USERNAME.github.io/REPO_NAME/`
