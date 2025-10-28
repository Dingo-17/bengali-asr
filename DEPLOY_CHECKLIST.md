# 🚀 Quick Deployment Checklist

Copy and paste these commands to deploy your website to GitHub Pages in minutes!

## ✅ Prerequisites

- [ ] GitHub account (create at https://github.com/join if needed)
- [ ] Git installed (`git --version` to check)
- [ ] Website tested locally ✅ (already running at http://localhost:8080)

## 📋 Step-by-Step Commands

### Step 1: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `bengali-dialect-transcription` (or your choice)
3. Description: "Production-ready ASR system for Bengali dialects"
4. Keep it Public (for free GitHub Pages)
5. **DO NOT** check "Initialize with README" (you already have one)
6. Click "Create repository"

### Step 2: Deploy Using Automated Script

```bash
# Navigate to project directory
cd /Users/digantohaque/python/BracV1

# Run deployment script
./docs/deploy.sh
```

The script will:
- Test the site locally first
- Set up git and .gitignore
- Ask for your GitHub username and repo name
- Update repository links automatically
- Push to GitHub
- Give you final instructions

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Source":
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**
6. Wait 2-5 minutes

### Step 4: Access Your Live Site

Your website will be at:
```
https://YOUR_USERNAME.github.io/bengali-dialect-transcription/
```

## 🔄 Alternative: Manual Deployment

If you prefer manual control:

```bash
# 1. Navigate to project
cd /Users/digantohaque/python/BracV1

# 2. Initialize git (if not done)
git init

# 3. Create .gitignore
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
data/raw/
data/processed/
models/*.pt
models/*.bin
models/whisper-*
*.wav
*.mp3
logs/
.env
.DS_Store
EOF

# 4. Add all files
git add .

# 5. Commit
git commit -m "Initial commit: Bengali ASR system with website"

# 6. Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 7. Push
git branch -M main
git push -u origin main
```

Then enable GitHub Pages as described in Step 3 above.

## 🎯 Quick Deploy to Other Platforms

### Netlify (Fastest - No Git Required)

```bash
# Install Netlify CLI (one-time only)
npm install -g netlify-cli

# Deploy
cd /Users/digantohaque/python/BracV1/docs
netlify deploy

# Follow prompts, then deploy to production
netlify deploy --prod
```

Or drag & drop: https://app.netlify.com/drop

### Vercel

```bash
# Install Vercel CLI (one-time only)
npm install -g vercel

# Deploy
cd /Users/digantohaque/python/BracV1/docs
vercel
```

## ✅ Post-Deployment Checklist

After deploying:

- [ ] Visit your live site URL
- [ ] Test on mobile device (or use browser DevTools)
- [ ] Check all navigation links work
- [ ] Verify GitHub repository link is correct
- [ ] Test drag-and-drop demo interface
- [ ] Share the link with colleagues!

## 🔧 Update Content Later

To update your deployed website:

```bash
cd /Users/digantohaque/python/BracV1

# Make changes to files in docs/

# Commit and push
git add docs/
git commit -m "Update website content"
git push

# Changes will be live in 1-2 minutes
```

## 🐛 Common Issues

### "Permission denied" when pushing to GitHub

**Solution:** You need a Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all checkboxes)
4. Copy the token
5. When git asks for password, paste the token (not your GitHub password)

### GitHub Pages shows 404

**Solutions:**
- Wait 5 minutes (first deployment takes time)
- Check Settings → Pages → Source is set to `main` branch, `/docs` folder
- Ensure repository is Public (or you have GitHub Pro for private repos)
- Clear browser cache

### CSS/JS not loading on live site

**Solution:** File paths issue
- All paths in HTML should be relative (not absolute)
- Already correct in your files, but if you edit, avoid paths starting with `/`

## 📞 Need Help?

- **Documentation:** `docs/DEPLOYMENT_GUIDE.md` (comprehensive)
- **Website Docs:** `docs/README.md`
- **Project Docs:** Main `README.md`
- **Email:** datasci@brac.net

## 🎉 That's It!

Your website is production-ready. Just run the deployment script and follow the prompts!

```bash
./docs/deploy.sh
```

**Estimated time:** 5-10 minutes from start to live website!
