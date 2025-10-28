# 🚀 Getting Started - Bengali ASR System

Welcome! This guide will help you get your Bengali ASR system live on the internet in under 20 minutes.

## 📋 What You'll Need

- [ ] GitHub account (free) - Sign up at https://github.com
- [ ] Railway.app account (free) - Sign up at https://railway.app
- [ ] Terminal/Command Line access
- [ ] This repository on your computer

**No coding experience required!** Just follow the steps below.

---

## 🎯 Goal

By the end of this guide, you'll have:

1. ✅ A live website at: `https://yourusername.github.io/bengali-asr/`
2. ✅ A working API at: `https://yourapp.up.railway.app`
3. ✅ Fully functional Bengali speech-to-text transcription

---

## 📖 Step-by-Step Guide

### Step 1: Create GitHub Repository (5 minutes)

1. **Go to GitHub**: https://github.com/new
2. **Fill in details**:
   - Repository name: `bengali-asr` (or any name you like)
   - Description: "Bengali Dialect Speech Recognition System"
   - Make it **Public**
3. **Click**: "Create repository"
4. **Copy the repository URL**: Something like `https://github.com/yourusername/bengali-asr.git`

### Step 2: Push Your Code to GitHub (3 minutes)

Open Terminal and run these commands **one by one**:

```bash
# Navigate to the project folder
cd /Users/digantohaque/python/BracV1

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit - Bengali ASR system"

# Connect to your GitHub repository (use YOUR URL from Step 1)
git remote add origin https://github.com/YOUR_USERNAME/bengali-asr.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Troubleshooting:**
- If asked for credentials, use your GitHub username and password
- If using 2FA, create a Personal Access Token (Settings → Developer settings → Personal access tokens)

### Step 3: Deploy Backend to Railway (5 minutes)

1. **Go to Railway**: https://railway.app

2. **Sign In**: Click "Login with GitHub"

3. **Create New Project**:
   - Click "New Project"
   - Click "Deploy from GitHub repo"
   - Select your `bengali-asr` repository
   - Railway will automatically detect it's a Python project

4. **Wait for Deployment** (2-3 minutes):
   - Watch the build logs (optional)
   - Look for "Build successful" and "Deploy successful"

5. **Get Your API URL**:
   - Click "Settings" tab
   - Find "Domains" section
   - Copy the URL (looks like: `https://bengali-asr-production-xxxx.up.railway.app`)
   - **SAVE THIS URL** - you'll need it next!

6. **Test Your Backend**:
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```
   
   Should return something like:
   ```json
   {"status":"ok","model_loaded":true,...}
   ```

### Step 4: Update Frontend with Backend URL (2 minutes)

1. **Open the file** `docs/script.js` in any text editor

2. **Find line 2**, which looks like:
   ```javascript
   const API_URL = 'http://localhost:8000';
   ```

3. **Replace it with your Railway URL**:
   ```javascript
   const API_URL = 'https://your-railway-url.up.railway.app';
   ```
   
   **Important:** Use YOUR actual Railway URL from Step 3!

4. **Save the file**

### Step 5: Push Updated Code (1 minute)

```bash
# Add the changed file
git add docs/script.js

# Commit the change
git commit -m "Update API URL for production"

# Push to GitHub
git push origin main
```

### Step 6: Enable GitHub Pages (3 minutes)

1. **Go to your repository** on GitHub

2. **Click "Settings"** tab (top right)

3. **Click "Pages"** in the left sidebar

4. **Under "Source"**:
   - Branch: Select **main**
   - Folder: Select **/docs**
   - Click **Save**

5. **Wait 2-3 minutes** for GitHub to build your site

6. **Find your URL**:
   - GitHub will show: "Your site is published at..."
   - Copy this URL: `https://YOUR_USERNAME.github.io/bengali-asr/`

### Step 7: Test Your Live Website! 🎉

1. **Open your GitHub Pages URL** in a browser

2. **Navigate to "Try Demo"** section (scroll down or click nav link)

3. **Upload an audio file**:
   - Click "Choose Audio File" or drag & drop
   - Supported formats: WAV, MP3, OGG, FLAC, M4A
   - Maximum size: 10MB

4. **Click "Transcribe"**

5. **See the magic!** 
   - Your audio is sent to the Railway backend
   - The AI model transcribes it
   - The Bengali text appears on screen

**Success!** 🎉 Your Bengali ASR system is now live!

---

## 🧪 Testing

### Quick Test Checklist

- [ ] Website loads at your GitHub Pages URL
- [ ] No console errors (press F12 to check)
- [ ] Can navigate to different sections
- [ ] Works on mobile (try on your phone)
- [ ] Can upload audio file
- [ ] Transcription button works
- [ ] Transcription text appears

### Test with Sample Audio

If you don't have Bengali audio files:

1. Record yourself saying something in Bengali
2. Save as WAV or MP3
3. Upload and test

Or use text-to-speech tools to generate sample audio.

---

## 🎨 Customization (Optional)

### Change Website Colors

1. Open `docs/styles.css`
2. Find the `:root` section at the top:
   ```css
   :root {
       --primary-color: #1e3a8a;    /* Change this */
       --secondary-color: #10b981;  /* And this */
   }
   ```
3. Replace with your preferred colors
4. Save, commit, and push to GitHub

### Change Website Text

1. Open `docs/index.html`
2. Edit any text you see
3. Save, commit, and push to GitHub

### Add Your Logo

1. Add your logo image to `docs/` folder
2. In `index.html`, find the logo section
3. Replace the emoji with:
   ```html
   <img src="your-logo.png" alt="Logo" style="height: 40px;">
   ```

---

## 🔧 Maintenance

### Update Your Website

```bash
# Make changes to files in docs/ folder
# Then:

git add .
git commit -m "Description of changes"
git push origin main

# Wait 2-3 minutes for GitHub Pages to rebuild
```

### Update Backend

Just push to GitHub - Railway auto-deploys!

```bash
# Make changes to inference/server.py or other files
# Then:

git add .
git commit -m "Update backend"
git push origin main

# Railway automatically rebuilds and redeploys
```

### Check Backend Logs

1. Go to Railway dashboard
2. Click on your project
3. Click "Deployments"
4. Click on the latest deployment
5. View logs

---

## 🆘 Common Issues

### Issue: "Failed to fetch" error when transcribing

**Solution:**
1. Check if backend is running:
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```
2. Verify API URL in `docs/script.js` matches your Railway URL
3. Check Railway logs for errors

### Issue: GitHub Pages shows 404

**Solution:**
1. Wait 2-3 minutes after enabling Pages
2. Check Settings → Pages is set to `/docs` folder
3. Verify files exist in the `docs/` folder
4. Try clearing browser cache

### Issue: Changes don't appear on website

**Solution:**
1. Make sure you pushed to GitHub: `git push origin main`
2. Wait 2-3 minutes for GitHub to rebuild
3. Clear browser cache (Cmd/Ctrl + Shift + R)
4. Check if changes are on GitHub.com

### Issue: Backend deployment fails on Railway

**Solution:**
1. Check Railway build logs for error messages
2. Verify `requirements.txt` exists and is valid
3. Check that Python version is compatible (3.10+)
4. Try redeploying from Railway dashboard

---

## 📊 Usage Limits (Free Tiers)

### GitHub Pages
- ✅ 100 GB bandwidth/month
- ✅ 10 builds per hour
- ✅ Perfect for static websites

### Railway (Free Tier)
- ✅ $5 free credit/month
- ✅ ~500 hours of uptime
- ⚠️ May sleep after inactivity
- ⚠️ Limited to 512MB RAM

**Tip:** If you exceed limits, upgrade or use Render.com (alternative deployment guide available).

---

## 🎓 Learning Resources

### Want to Learn More?

- **Git/GitHub**: https://guides.github.com/
- **Python**: https://www.python.org/about/gettingstarted/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Machine Learning**: https://www.coursera.org/learn/machine-learning

### Project Documentation

- `README.md` - Full project overview
- `QUICKSTART.md` - Technical quickstart
- `TROUBLESHOOTING.md` - Detailed troubleshooting
- `DEPLOYMENT_SUMMARY.md` - Deployment options

---

## 🚀 Next Steps

Now that your system is live:

1. **Share it!** 
   - Send the link to colleagues
   - Get feedback from users
   - Share on social media

2. **Monitor Performance**:
   - Check Railway dashboard for usage
   - Monitor GitHub Pages analytics (if enabled)

3. **Improve**:
   - Add more features
   - Optimize the model
   - Improve the UI/UX

4. **Scale**:
   - Upgrade to paid tier for more resources
   - Add custom domain
   - Implement analytics

---

## ✅ Success Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Backend deployed to Railway
- [ ] Backend health check passes
- [ ] Frontend API URL updated
- [ ] Changes pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Website is live and accessible
- [ ] Can upload and transcribe audio
- [ ] Tested on multiple devices

---

## 🎉 Congratulations!

You've successfully deployed a production-ready Bengali ASR system!

**Your Links:**
- Website: `https://YOUR_USERNAME.github.io/bengali-asr/`
- API: `https://your-railway-url.up.railway.app`
- Repository: `https://github.com/YOUR_USERNAME/bengali-asr`

Share your achievement! Post on LinkedIn, Twitter, or show your colleagues!

---

## 💬 Need Help?

If you run into issues:

1. Check the troubleshooting section above
2. Review the detailed documentation in the repository
3. Check Railway/GitHub logs for error messages
4. Use the test tool: `docs/test-connection.html`

**Remember:** Every expert was once a beginner. You've got this! 💪
