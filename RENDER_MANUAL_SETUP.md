# 🚨 RENDER DEPLOYMENT FIX - Manual Setup Required

## Problem
The existing Render service is caching old configurations and trying to load the full model instead of using the demo server.

## Solution: Create a NEW Web Service

Follow these steps to create a fresh deployment that will work:

---

## Step 1: Delete Old Service (Optional)

1. Go to https://dashboard.render.com
2. Find your current service `bengali-asr-api`
3. Click on it → **Settings** (bottom left)
4. Scroll down → Click **Delete Web Service**
5. Confirm deletion

---

## Step 2: Create NEW Web Service

### 2.1 Start New Service
1. Go to https://dashboard.render.com
2. Click **New +** (top right)
3. Select **Web Service**

### 2.2 Connect Repository
1. Click **Configure account** next to GitHub
2. Select your repository: `Dingo-17/bengali-asr`
3. Click **Connect**

### 2.3 Configure Service Settings

Enter these settings **EXACTLY**:

```
Name:                bengali-asr-demo
Region:              Oregon (US West)
Branch:              main
Runtime:             Python 3
Build Command:       pip install --upgrade pip && pip install fastapi uvicorn python-multipart
Start Command:       uvicorn inference.demo_server:app --host 0.0.0.0 --port $PORT --workers 1
Instance Type:       Free
```

### 2.4 Advanced Settings (IMPORTANT!)

Click **Advanced** and set:

**Environment Variables:**
```
Key: PYTHON_VERSION      Value: 3.10.13
Key: PYTHONUNBUFFERED    Value: 1
```

**Health Check Path:**
```
/health
```

**Auto-Deploy:**
✅ Yes (enabled)

---

## Step 3: Deploy

1. Click **Create Web Service** at the bottom
2. Wait for deployment (~3-5 minutes)
3. Watch the logs - you should see:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ```

---

## Step 4: Test

Once deployed, your service URL will be:
```
https://bengali-asr-demo.onrender.com
```

Test it:

### Health Check
```bash
curl https://bengali-asr-demo.onrender.com/health
```

Expected response:
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

### API Documentation
Visit: https://bengali-asr-demo.onrender.com/docs

---

## Step 5: Update Frontend

Once your backend is live, update the frontend:

```bash
# Edit docs/script.js line 2:
const API_URL = 'https://bengali-asr-demo.onrender.com';

# Commit and push:
git add docs/script.js
git commit -m "Update API URL to new Render service"
git push origin main
```

---

## Why Manual Setup?

The `render.yaml` file works for NEW deployments, but when a service already exists, Render might:
- Cache old environment variables
- Use previous build settings
- Ignore YAML changes

Creating a fresh service ensures a clean deployment.

---

## Troubleshooting

### If deployment still fails:

1. **Check Logs** in Render dashboard
2. **Verify Start Command** uses `demo_server` not `server`
3. **Check Build Command** only installs fastapi, uvicorn, python-multipart
4. **Ensure** NO environment variables point to model paths

### If you see model loading errors:

The service is still trying to use `server.py`. Double-check:
- Start command is: `uvicorn inference.demo_server:app ...`
- NOT: `uvicorn inference.server:app ...`

---

## Alternative: Test Locally First

Before deploying to Render, test the demo server locally:

```bash
cd /Users/digantohaque/python/BracV1
./test_demo_server.sh
```

Then visit http://localhost:8000/health

If this works locally, the same will work on Render with the correct configuration.

---

## Summary Checklist

- [ ] Delete old service (or create new one with different name)
- [ ] Create new web service from GitHub
- [ ] Set Build Command: `pip install --upgrade pip && pip install fastapi uvicorn python-multipart`
- [ ] Set Start Command: `uvicorn inference.demo_server:app --host 0.0.0.0 --port $PORT --workers 1`
- [ ] Set Runtime: Python 3
- [ ] Set Health Check: `/health`
- [ ] Click Create Web Service
- [ ] Wait for deployment
- [ ] Test health endpoint
- [ ] Update frontend with new URL
- [ ] Enable GitHub Pages
- [ ] Test complete system

---

## Need Help?

If you're still seeing errors:

1. **Screenshot** the Render service settings page
2. **Copy** the full deployment logs
3. **Share** the exact error message

The demo server is incredibly simple - it WILL work with the correct settings! 🚀

---

**Next Step:** Go to Render dashboard and create a fresh web service following the steps above.
