# 🆓 FREE Deployment Guide - Render.com

## ✅ Why Render.com?

- 💰 **100% FREE** tier (no credit card required initially)
- 🚀 Easy deployment from GitHub
- 🔄 Auto-deploys on git push
- 📊 Free SSL/HTTPS
- 🌍 Global CDN

**Railway requires payment after $5 credit. Render.com is FREE forever (with limitations).**

---

## 🚀 Complete FREE Deployment Steps

### STEP 1: Create GitHub Repository (1 minute)

1. **Go to**: https://github.com/new
2. **Repository name**: `bengali-asr`
3. **Description**: Bengali Dialect Speech Recognition System
4. **Visibility**: ✅ **PUBLIC**
5. **Important**: Do NOT check "Initialize with README"
6. **Click**: "Create repository"

---

### STEP 2: Push to GitHub (2 minutes)

**Easiest method - GitHub CLI:**
```bash
# Install GitHub CLI (if not installed)
brew install gh

# Login to GitHub
gh auth login

# Push your code
cd /Users/digantohaque/python/BracV1
git push -u origin main
```

**Alternative - Personal Access Token:**
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic) with `repo` scope
3. Copy token
4. Run:
   ```bash
   cd /Users/digantohaque/python/BracV1
   git push -u origin main
   # Username: Dingo-17
   # Password: [paste token]
   ```

---

### STEP 3: Deploy Backend to Render.com (FREE) 🎉

1. **Go to**: https://render.com

2. **Sign Up**: Click "Get Started" → Sign up with GitHub

3. **New Web Service**:
   - Click "New +" button (top right)
   - Select "Web Service"

4. **Connect Repository**:
   - Click "Connect account" if needed
   - Find and select: `Dingo-17/bengali-asr`
   - Click "Connect"

5. **Configure Service**:
   - **Name**: `bengali-asr` (or any name you like)
   - **Region**: Choose closest to you (Oregon, Frankfurt, Singapore)
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn inference.server:app --host 0.0.0.0 --port $PORT --workers 2`

6. **Choose Plan**:
   - Select: ✅ **Free** (0$/month)
   - Limitations: 
     - App sleeps after 15 min of inactivity
     - 750 hours/month free
     - 512 MB RAM
     - Shared CPU

7. **Environment Variables** (Optional):
   - Click "Advanced"
   - Add environment variable:
     - `MODEL_TYPE` = `wav2vec2`
     - `PYTHON_VERSION` = `3.10`

8. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Watch the logs (deployment progress)

9. **Get Your URL**:
   - After deployment, you'll see your URL at the top
   - Format: `https://bengali-asr.onrender.com`
   - **Copy this URL!**

---

### STEP 4: Update Frontend API URL (1 minute)

1. **Edit** `docs/script.js` line 2:
   ```javascript
   const API_URL = 'https://bengali-asr.onrender.com';  // Your Render URL
   ```

2. **Commit and push**:
   ```bash
   cd /Users/digantohaque/python/BracV1
   git add docs/script.js
   git commit -m "Update API URL to Render.com deployment"
   git push origin main
   ```

---

### STEP 5: Enable GitHub Pages (1 minute)

1. **Go to**: https://github.com/Dingo-17/bengali-asr/settings/pages
2. **Under "Source"**:
   - Branch: `main`
   - Folder: `/docs`
3. **Click**: "Save"
4. **Wait**: 2-3 minutes for build

**Your site will be live at**: `https://dingo-17.github.io/bengali-asr/`

---

## 🧪 Test Your FREE Deployment

### Test Backend
```bash
curl https://bengali-asr.onrender.com/health
```

Should return:
```json
{
  "status": "ok",
  "model_loaded": true,
  "device": "cpu"
}
```

### Test Frontend

1. Visit: `https://dingo-17.github.io/bengali-asr/`
2. Go to "Try Demo" section
3. Upload Bengali audio file
4. Click "Transcribe"
5. See transcription! 🎉

---

## 💡 Render.com FREE Tier Details

### What's Included (FREE):
✅ 750 hours/month (enough for most use cases)
✅ Auto-deploy from GitHub
✅ Free SSL (HTTPS)
✅ Custom domains
✅ Persistent disks
✅ Environment variables

### Limitations:
⚠️ Sleeps after 15 min inactivity (takes 30-60s to wake up)
⚠️ 512 MB RAM (may be tight for large models)
⚠️ Shared CPU (slower inference)

### Handling Sleep Mode:
- First request after sleep takes 30-60 seconds
- Subsequent requests are fast
- Users see "loading" during wake-up
- **Solution**: Keep it awake with a cron job (see below)

---

## 🔄 Keep Your Service Awake (Optional)

To prevent sleeping, ping your service every 14 minutes:

### Option 1: Use UptimeRobot (FREE)
1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Add monitor:
   - URL: `https://bengali-asr.onrender.com/health`
   - Interval: 5 minutes
   - Monitor type: HTTP(s)

### Option 2: GitHub Actions (FREE)
Create `.github/workflows/keep-alive.yml`:
```yaml
name: Keep Render Service Awake

on:
  schedule:
    - cron: '*/14 * * * *'  # Every 14 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render
        run: curl https://bengali-asr.onrender.com/health
```

---

## 📊 Render vs Railway Comparison

| Feature | Render (FREE) | Railway (FREE) |
|---------|---------------|----------------|
| **Cost** | ✅ FREE forever | 💳 $5 credit then paid |
| **Deployment** | ✅ Auto-deploy | ✅ Auto-deploy |
| **Sleep** | ⚠️ After 15 min | ✅ No sleep (credit) |
| **RAM** | 512 MB | 512 MB |
| **CPU** | Shared | Shared |
| **Best for** | Low traffic | Active development |

**For your use case**: Render is PERFECT! ✅

---

## 🎯 Your FREE Deployment URLs

| Service | URL |
|---------|-----|
| **Frontend** | https://dingo-17.github.io/bengali-asr/ |
| **Backend** | https://bengali-asr.onrender.com |
| **API Docs** | https://bengali-asr.onrender.com/docs |
| **Health** | https://bengali-asr.onrender.com/health |
| **GitHub** | https://github.com/Dingo-17/bengali-asr |

---

## 🆘 Troubleshooting

### "This service is currently unavailable"
→ Service is waking from sleep. Wait 30-60 seconds and refresh.

### Deployment failed
→ Check Render logs:
  - Go to Render dashboard
  - Click on your service
  - Click "Logs" tab
  - Look for error messages

### Out of memory
→ Model too large for free tier
  **Solutions**:
  1. Use quantized model (smaller)
  2. Upgrade to paid tier ($7/month)
  3. Use different deployment (Hugging Face Spaces)

### Backend is slow
→ Normal on free tier (shared CPU)
  - First request: 30-60s (wake up)
  - Subsequent requests: 5-10s (inference)
  - Upgrade for faster performance

---

## 💰 Cost Comparison

### Render.com FREE (Your current plan)
- **Cost**: $0/month ✅
- **Perfect for**: Testing, demos, low traffic
- **Limitations**: Sleeps after 15 min

### Render.com Starter ($7/month)
- **Cost**: $7/month
- **Benefits**: 
  - No sleep
  - More RAM (1 GB+)
  - Faster CPU
- **When to upgrade**: If you get regular traffic

### Railway ($5/month minimum)
- **Cost**: $5-20/month (usage-based)
- **Benefits**: 
  - No sleep
  - Better performance
- **When to use**: Production apps with consistent traffic

**For FREE deployment**: Stick with Render! ✅

---

## 🚀 Quick Commands

```bash
# Push to GitHub (after creating repo)
cd /Users/digantohaque/python/BracV1
git push -u origin main

# Update API URL (after Render deployment)
# Edit docs/script.js line 2, then:
git add docs/script.js
git commit -m "Update API URL to Render"
git push origin main

# Test backend
curl https://bengali-asr.onrender.com/health

# Check deployment logs
# Go to: https://dashboard.render.com
```

---

## ✅ Deployment Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Signed up for Render.com (FREE)
- [ ] Created Web Service on Render
- [ ] Configured build/start commands
- [ ] Selected FREE plan
- [ ] Deployment completed (check logs)
- [ ] Copied Render URL
- [ ] Updated `docs/script.js` with Render URL
- [ ] Pushed API URL update to GitHub
- [ ] Enabled GitHub Pages
- [ ] Frontend loads at: https://dingo-17.github.io/bengali-asr/
- [ ] Backend health check passes
- [ ] Can upload and transcribe audio
- [ ] **System is LIVE and 100% FREE!** 🎉

---

## 🎉 Success!

Once complete, you'll have:

✅ **FREE frontend hosting** (GitHub Pages)
✅ **FREE backend hosting** (Render.com)
✅ **No credit card required** (initially)
✅ **Auto-deploy on git push**
✅ **Professional URLs with HTTPS**

All completely FREE! 🆓

---

## 🔄 Future Upgrades (When Needed)

If you outgrow the free tier:

1. **Render Starter** ($7/month)
   - No sleep
   - More resources
   - Best value

2. **Vercel + Serverless Backend**
   - Frontend: FREE on Vercel
   - Backend: AWS Lambda (free tier)

3. **Hugging Face Spaces** (FREE)
   - FREE GPU for ML models
   - Community platform

But start with FREE Render! ✅

---

**Ready to deploy? Follow the steps above!**

**Total Cost**: $0/month 🎉
**Total Time**: 10-15 minutes
**Difficulty**: Easy!
