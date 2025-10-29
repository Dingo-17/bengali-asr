# 🚀 FRESH RENDER SETUP - Step by Step

You deleted the old project - **perfect!** Now let's create a new one that will work.

---

## ✅ Quick Setup (Follow These Exact Steps)

### Step 1: Go to Render Dashboard
1. Open: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"Web Service"**

---

### Step 2: Connect Your GitHub Repository

1. You'll see "Connect a repository"
2. Find and click: **Dingo-17/bengali-asr**
3. Click **"Connect"**

*(If you don't see it, click "Configure account" and grant Render access to the repo)*

---

### Step 3: Configure the Service

Fill in these **EXACT** values:

#### Basic Settings:
```
Name:                bengali-asr-demo
Region:              Oregon (US West)
Branch:              main
Runtime:             Python 3
```

#### Build & Deploy:
```
Build Command:       pip install --upgrade pip && pip install fastapi uvicorn python-multipart

Start Command:       uvicorn inference.demo_server:app --host 0.0.0.0 --port $PORT --workers 1
```

#### Instance Type:
```
Plan:                Free
```

---

### Step 4: Advanced Settings

Click **"Advanced"** button to expand, then add:

#### Environment Variables:
Click **"Add Environment Variable"** for each:

```
Key: PYTHON_VERSION          Value: 3.10.13
Key: PYTHONUNBUFFERED        Value: 1
```

#### Health Check Path:
```
/health
```

#### Auto-Deploy:
```
✅ Yes (checked)
```

---

### Step 5: Create!

1. Scroll to bottom
2. Click **"Create Web Service"**
3. **Wait and watch the logs!**

You should see:
```
==> Building...
==> Installing dependencies
==> Build successful
==> Deploying...
INFO:     Uvicorn running on http://0.0.0.0:10000
INFO:     Started server process
```

**This should take 3-5 minutes.**

---

## ✅ Verify It Works

Once you see "Deploy successful", your URL will be:
```
https://bengali-asr-demo.onrender.com
```

### Test the Health Endpoint:

Open a new terminal and run:
```bash
curl https://bengali-asr-demo.onrender.com/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "mode": "demo",
  "tier": "free",
  "message": "Demo mode - returns mock transcriptions",
  "limitations": {
    "max_file_size_mb": 5.0,
    "max_duration_seconds": 30,
    "ram": "512MB",
    "note": "Upgrade for actual transcription"
  }
}
```

### Or visit in browser:
```
https://bengali-asr-demo.onrender.com/docs
```

You should see the FastAPI interactive documentation!

---

## 🎯 What to Watch For

### ✅ GOOD LOGS (Success):
```
==> Build successful
==> Deploying...
INFO:     Uvicorn running on http://0.0.0.0:10000
INFO:     Started server process
==> Your service is live 🎉
```

### ❌ BAD LOGS (Problem):
If you see:
- "Loading model..." → Wrong server (should be demo_server)
- "Child process died" → Memory issue (check it's using demo_server)
- No logs at all → Auto-deploy might be off

---

## 🔧 Troubleshooting

### If Nothing Happens:
1. Check Auto-Deploy is **ON** in Settings
2. Try **Manual Deploy**: Click "Manual Deploy" → "Deploy latest commit"

### If It Tries to Load Model:
1. Go to service → **Settings**
2. Check **Start Command** is: `uvicorn inference.demo_server:app --host 0.0.0.0 --port $PORT --workers 1`
3. NOT: `server.py` or `server_lightweight.py`

### If Build Fails:
1. Check logs for specific error
2. Verify Build Command is correct
3. Make sure repo is pushed to GitHub

---

## ⏭️ After Successful Deployment

Once you see the health check working:

### 1. Update Frontend
```bash
cd /Users/digantohaque/python/BracV1
nano docs/script.js
```

Change line 2 to:
```javascript
const API_URL = 'https://bengali-asr-demo.onrender.com';
```

Save and push:
```bash
git add docs/script.js
git commit -m "Update API URL to Render backend"
git push origin main
```

### 2. Enable GitHub Pages
1. Go to: https://github.com/Dingo-17/bengali-asr
2. Click **Settings** → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** → Folder: **/docs**
5. Click **Save**
6. Wait 2-3 minutes

### 3. Test Your Live Site!
Visit: https://Dingo-17.github.io/bengali-asr/

Upload an audio file and click "Transcribe" - you should see:
```
আমি বাংলায় গান গাই (Demo Mode)
```

---

## 📋 Quick Checklist

- [ ] Deleted old Render project ✅ (You did this!)
- [ ] Created new web service
- [ ] Set Build Command correctly
- [ ] Set Start Command to `demo_server`
- [ ] Set Python version to 3.10.13
- [ ] Added health check path
- [ ] Clicked "Create Web Service"
- [ ] Watched logs for success
- [ ] Tested health endpoint
- [ ] Updated frontend API URL
- [ ] Enabled GitHub Pages
- [ ] Tested live site

---

## 🆘 If You Get Stuck

**Copy and paste:**
1. The **exact error message** from Render logs
2. Your **Start Command** from Render settings
3. Your **Build Command** from Render settings

---

## 🎉 Success Criteria

You'll know it worked when:
1. ✅ Render shows "Your service is live"
2. ✅ Health endpoint returns JSON
3. ✅ `/docs` page loads with FastAPI UI
4. ✅ Frontend site loads on GitHub Pages
5. ✅ Can upload audio and get demo transcription

---

**Ready? Go to https://dashboard.render.com and click "New +" !** 🚀

Let me know when you get to the logs screen!
