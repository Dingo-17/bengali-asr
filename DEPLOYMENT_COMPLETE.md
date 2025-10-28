# 🚀 Complete Deployment Guide

This guide will help you deploy both the frontend (GitHub Pages) and backend (API server) for the Bengali ASR system.

## 📋 Prerequisites

- Python 3.8+
- Git
- GitHub account
- (Optional) Account on Render.com or Railway.app for free backend hosting

## 🎯 Quick Start (5 minutes)

### Option 1: Automated Deployment

```bash
cd /Users/digantohaque/python/BracV1
./deploy-full.sh
```

Follow the prompts to:
1. Set up GitHub repository
2. Configure API URL
3. Deploy frontend to GitHub Pages
4. Get backend deployment instructions

### Option 2: Manual Deployment

Follow the steps below for full control.

---

## 📦 Part 1: Deploy Frontend to GitHub Pages

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `bengali-asr` (or your choice)
3. Description: "Bengali Dialect Transcription System"
4. Set to **Public** (required for free GitHub Pages)
5. **DO NOT** check "Initialize with README"
6. Click "Create repository"

### Step 2: Update API URL

Edit `docs/script.js` and change line 2:

```javascript
const API_URL = 'YOUR_API_URL_HERE';  // e.g., 'https://your-app.onrender.com'
```

### Step 3: Push to GitHub

```bash
cd /Users/digantohaque/python/BracV1

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Bengali ASR system"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Source":
   - Branch: `main`
   - Folder: `/docs`
4. Click **Save**
5. Wait 2-5 minutes

Your site will be live at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

---

## 🖥️ Part 2: Deploy Backend API

You have 3 options:

### Option A: Local Testing (Easiest)

Perfect for testing before deploying:

```bash
cd /Users/digantohaque/python/BracV1/inference

# Run the simple server
python3 simple_server.py
```

The API will be at `http://localhost:8000`

**Note:** This only works locally, not for the deployed GitHub Pages site.

---

### Option B: Deploy to Render.com (Free, Recommended)

Render.com offers free hosting for backend APIs.

#### 1. Create Render Account
- Go to https://dashboard.render.com/
- Sign up with GitHub

#### 2. Create New Web Service
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository

#### 3. Configure Service
```
Name: bengali-asr-api
Environment: Python 3
Branch: main
Build Command: pip install -r requirements.txt
Start Command: cd inference && python simple_server.py
Instance Type: Free
```

#### 4. Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:
```
MODEL_TYPE=whisper
PYTHON_VERSION=3.11
```

#### 5. Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Your API URL will be: `https://your-app-name.onrender.com`

#### 6. Update Frontend
Edit `docs/script.js`:
```javascript
const API_URL = 'https://your-app-name.onrender.com';
```

Then push changes:
```bash
git add docs/script.js
git commit -m "Update API URL"
git push
```

---

### Option C: Deploy to Railway.app (Free Alternative)

#### 1. Create Railway Account
- Go to https://railway.app/
- Sign up with GitHub

#### 2. Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose your repository

#### 3. Configure
Railway auto-detects Python and will deploy automatically.

Add environment variables:
```
MODEL_TYPE=whisper
PORT=8000
```

#### 4. Get API URL
- Click on your deployment
- Copy the public URL (e.g., `https://your-app.up.railway.app`)

#### 5. Update Frontend
Same as Render.com - update `docs/script.js` with your Railway URL.

---

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl https://your-api-url.com/health

# Test transcription (replace with your audio file)
curl -X POST https://your-api-url.com/transcribe \
  -F "audio=@test.wav"
```

### Test Frontend

1. Go to your GitHub Pages URL
2. Click "Demo"
3. Upload a Bengali audio file
4. Check if transcription works

---

## 🔧 Troubleshooting

### Frontend Issues

**Problem:** GitHub Pages shows 404
**Solution:** 
- Check Settings → Pages is configured correctly
- Ensure `/docs` folder is selected
- Wait 5 minutes after enabling

**Problem:** CSS/JS not loading
**Solution:**
- Hard refresh browser (Cmd+Shift+R)
- Check browser console for errors
- Verify file paths are relative

### Backend Issues

**Problem:** API returns CORS error
**Solution:** 
- Ensure CORS is enabled in server code
- Check `allow_origins` includes your GitHub Pages URL

**Problem:** Transcription fails
**Solution:**
- Check API logs for errors
- Verify audio file format (WAV, MP3, M4A)
- Check file size (<10MB)

**Problem:** "API server not accessible"
**Solution:**
- Ensure backend is deployed and running
- Check API URL in `docs/script.js` is correct
- Test API health endpoint: `https://your-api/health`

---

## 📊 Cost Breakdown

### Free Tier Limits

**GitHub Pages:**
- ✅ Unlimited bandwidth
- ✅ 1GB storage
- ✅ Custom domain support

**Render.com Free:**
- ✅ 750 hours/month
- ⚠️ Spins down after 15 min inactivity (cold start)
- ✅ 512MB RAM
- ✅ Automatic HTTPS

**Railway.app Free:**
- ✅ $5 credit/month
- ✅ 500MB RAM
- ✅ Always on (no cold starts)

---

## 🎯 Next Steps

After deployment:

1. **Test thoroughly** with various Bengali audio files
2. **Monitor usage** on your hosting platform
3. **Set up custom domain** (optional)
4. **Add analytics** (Google Analytics, Plausible)
5. **Improve model** by training on more data

---

## 📞 Support

- Email: datasci@brac.net
- GitHub Issues: https://github.com/YOUR_USERNAME/REPO_NAME/issues
- Documentation: See main README.md

---

## ✅ Deployment Checklist

Frontend:
- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Enabled GitHub Pages
- [ ] Verified site is live
- [ ] Updated API URL in script.js

Backend:
- [ ] Chosen hosting platform
- [ ] Deployed API server
- [ ] Tested health endpoint
- [ ] Tested transcription endpoint
- [ ] Updated frontend with API URL

Final:
- [ ] End-to-end test (upload audio → get transcription)
- [ ] Checked on mobile device
- [ ] Shared link with team

---

**Estimated Time:** 15-30 minutes total

Good luck! 🚀
