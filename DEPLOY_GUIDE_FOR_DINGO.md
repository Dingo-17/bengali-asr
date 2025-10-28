# 🎯 Deployment Guide for Dingo-17

## ⚠️ IMPORTANT SECURITY NOTICE

**Please change your GitHub password immediately!**

1. Go to: https://github.com/settings/security
2. Click "Change password"
3. Create a strong, unique password
4. Enable Two-Factor Authentication (2FA) for extra security

**Why?** You shared your password publicly. Anyone who saw it could access your account.

---

## 🚀 How to Deploy Your Bengali ASR System

I've created a personalized deployment script for you. Here's what to do:

### Step 1: Change Your Password First! 🔒

**DO THIS NOW before anything else:**

```
1. Go to: https://github.com/settings/security
2. Change your password
3. Enable 2FA (highly recommended)
```

### Step 2: Run the Deployment Script

Once your password is changed, run this command:

```bash
cd /Users/digantohaque/python/BracV1
./deploy-for-dingo.sh
```

This script will:
- ✅ Set up Git with your username (Dingo-17)
- ✅ Create repository URL (https://github.com/Dingo-17/bengali-asr)
- ✅ Update frontend configuration
- ✅ Commit and push to GitHub
- ✅ Provide step-by-step instructions

### Step 3: Authenticate with GitHub

When the script asks for authentication, you have **3 safe options**:

#### Option A: Personal Access Token (Recommended) ⭐

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "Bengali ASR Deployment"
4. Select scopes: ✅ **repo** (all sub-options)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When git asks for password, **paste the token** (not your password!)

#### Option B: GitHub CLI (Easiest)

```bash
# Install GitHub CLI
brew install gh

# Login
gh auth login

# Then re-run the deployment script
./deploy-for-dingo.sh
```

#### Option C: SSH Key

Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

---

## 📋 Complete Deployment Checklist

### Before Running Script
- [ ] ⚠️ **Password changed on GitHub**
- [ ] ⚠️ **2FA enabled (recommended)**
- [ ] GitHub account accessible
- [ ] Terminal open in correct directory

### Run Script
- [ ] Run: `./deploy-for-dingo.sh`
- [ ] Choose backend platform (Railway recommended)
- [ ] Authenticate with GitHub (use token or gh CLI)
- [ ] Verify push was successful

### After Script
- [ ] Create GitHub repository (if it doesn't exist):
  - Go to: https://github.com/new
  - Name: `bengali-asr`
  - Public repository
  - Don't initialize with README
  - Create

- [ ] Enable GitHub Pages:
  - Go to: https://github.com/Dingo-17/bengali-asr/settings/pages
  - Source: Branch `main`, Folder `/docs`
  - Save

- [ ] Deploy Backend to Railway:
  - Go to: https://railway.app
  - Sign in with GitHub
  - New Project → Deploy from GitHub
  - Select: Dingo-17/bengali-asr
  - Copy Railway URL

- [ ] Update API URL (if using Railway):
  - Edit `docs/script.js` line 2
  - Change to Railway URL
  - Commit and push:
    ```bash
    git add docs/script.js
    git commit -m "Update API URL"
    git push
    ```

### Test Deployment
- [ ] Frontend: Visit https://dingo-17.github.io/bengali-asr/
- [ ] Backend: `curl https://your-app.up.railway.app/health`
- [ ] Upload test audio file
- [ ] Verify transcription works

---

## 🎯 Your Deployment URLs

After completing all steps:

**Frontend**: https://dingo-17.github.io/bengali-asr/
**Backend**: https://[your-railway-app].up.railway.app
**API Docs**: https://[your-railway-app].up.railway.app/docs

---

## 🆘 Troubleshooting

### "Authentication failed"
→ Use Personal Access Token (see Option A above)

### "Repository doesn't exist"
→ Create it at: https://github.com/new

### "Permission denied"
→ Make sure you're logged into the correct GitHub account

### "Push rejected"
→ Make sure repository exists and you have write access

### Need more help?
→ Check `GETTING_STARTED.md` or `TROUBLESHOOTING.md`

---

## ⚡ Quick Commands

```bash
# Deploy everything
./deploy-for-dingo.sh

# Check if backend is running
curl http://localhost:8000/health

# Push updates
git add .
git commit -m "Update"
git push

# View deployment logs
# Go to Railway dashboard
```

---

## 🔐 Security Best Practices

1. ✅ **Never share passwords** - Use tokens instead
2. ✅ **Enable 2FA** on GitHub
3. ✅ **Use strong, unique passwords**
4. ✅ **Rotate tokens periodically**
5. ✅ **Review account security regularly**

---

## ✨ Next Steps

1. **Change password NOW** ⚠️
2. Run: `./deploy-for-dingo.sh`
3. Follow on-screen instructions
4. Enable GitHub Pages
5. Deploy backend to Railway
6. Test your live site!

---

**Everything is ready for you! Just run the script after changing your password.**

For detailed help: `open GETTING_STARTED.md`
