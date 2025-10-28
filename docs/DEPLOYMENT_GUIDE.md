# Website Deployment Guide

This guide explains how to deploy the Bengali ASR website to GitHub Pages and other free hosting platforms.

## 📁 Website Files

The static website is located in the `docs/` directory:
- `index.html` - Main webpage with all sections
- `styles.css` - Complete styling and responsive design
- `script.js` - Interactive features and demo functionality

## 🚀 Deployment Options

### Option 1: GitHub Pages (Recommended)

GitHub Pages is the easiest way to host this static website for free.

#### Step 1: Push to GitHub

1. Initialize git repository (if not already done):
```bash
cd /Users/digantohaque/python/BracV1
git init
```

2. Create a `.gitignore` file:
```bash
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Data and Models
data/raw/
data/processed/
models/*.pt
models/*.pth
models/*.bin
models/whisper-*
*.wav
*.mp3
*.m4a

# Logs
logs/
*.log

# Environment
.env
.DS_Store
EOF
```

3. Add and commit files:
```bash
git add .
git commit -m "Initial commit: Bengali ASR system with website"
```

4. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name it: `bengali-dialect-transcription` (or your preferred name)
   - Don't initialize with README (you already have one)
   - Click "Create repository"

5. Link and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/bengali-dialect-transcription.git
git branch -M main
git push -u origin main
```

#### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. Under "Source", select:
   - **Branch**: `main`
   - **Folder**: `/docs`
4. Click **Save**
5. Wait 2-5 minutes for deployment

Your site will be live at:
```
https://YOUR_USERNAME.github.io/bengali-dialect-transcription/
```

#### Step 3: Configure Custom Domain (Optional)

If you own a domain:
1. Add a `CNAME` file in `docs/`:
```bash
echo "yourdomain.com" > docs/CNAME
```

2. In your domain registrar's DNS settings, add:
   - Type: `CNAME`
   - Name: `www` (or `@` for root)
   - Value: `YOUR_USERNAME.github.io`

3. In GitHub Pages settings, enter your custom domain

---

### Option 2: Netlify

Netlify offers free hosting with automatic deployments.

#### Deploy via Drag & Drop:

1. Go to https://app.netlify.com/drop
2. Drag the `docs/` folder into the browser
3. Your site is live instantly!

#### Deploy via Git:

1. Sign up at https://netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect your GitHub repository
4. Configure:
   - **Branch**: `main`
   - **Base directory**: Leave empty
   - **Publish directory**: `docs`
5. Click **Deploy**

Your site will be live at: `https://random-name.netlify.app`

You can customize the subdomain or add a custom domain in settings.

---

### Option 3: Vercel

Vercel is another excellent free hosting option.

1. Sign up at https://vercel.com
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `docs`
5. Click **Deploy**

Your site will be live at: `https://your-project.vercel.app`

---

### Option 4: Cloudflare Pages

1. Sign up at https://pages.cloudflare.com
2. Click **"Create a project"** → **"Connect to Git"**
3. Select your repository
4. Configure:
   - **Build command**: Leave empty (static site)
   - **Build output directory**: `docs`
5. Click **"Save and Deploy"**

---

## 🧪 Local Testing

Before deploying, test the website locally:

### Option 1: Python HTTP Server

```bash
cd /Users/digantohaque/python/BracV1/docs
python3 -m http.server 8080
```

Then open: http://localhost:8080

### Option 2: VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### Option 3: Node.js HTTP Server

```bash
npx http-server docs -p 8080
```

---

## 🔧 Configuration

### Update Repository Links

The website currently points to:
```
https://github.com/BRAC/bengali-dialect-transcription
```

If your repository URL is different, update these in `docs/index.html`:

```bash
# Find and replace (macOS)
sed -i '' 's|https://github.com/BRAC/bengali-dialect-transcription|YOUR_REPO_URL|g' docs/index.html
```

Or manually search for all instances of the GitHub URL and update them.

### Enable Live Demo

The current website shows a demo placeholder. To connect it to a live backend:

1. Deploy the FastAPI server (see main README.md)
2. Update the API endpoint in `docs/script.js`:

```javascript
// Around line 80-90 in script.js
const API_URL = 'https://your-api-server.com/transcribe';  // Update this
```

3. Ensure CORS is enabled on your backend server:

```python
# In inference/server.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://YOUR_USERNAME.github.io"],  # Your website URL
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📱 Mobile Responsiveness

The website is fully responsive and works on:
- 📱 Mobile phones (320px+)
- 📱 Tablets (768px+)
- 💻 Laptops (1024px+)
- 🖥️ Desktops (1200px+)

Test responsive design:
1. Open in Chrome/Firefox
2. Press `F12` for DevTools
3. Click device toolbar icon (or `Ctrl+Shift+M`)
4. Select different device sizes

---

## 🎨 Customization

### Colors

Edit CSS variables in `docs/styles.css` (lines 7-16):

```css
:root {
    --primary-color: #2563eb;      /* Blue */
    --secondary-color: #10b981;     /* Green */
    --dark-bg: #1f2937;             /* Dark gray */
    /* ... etc */
}
```

### Fonts

The website uses Google Fonts (Noto Sans Bengali for Bengali text). To change:

1. Go to https://fonts.google.com
2. Select your fonts
3. Copy the `<link>` tag
4. Replace in `docs/index.html` (around line 10)
5. Update `font-family` in `docs/styles.css`

### Content

- **Hero stats**: Update in `<div class="hero-stats">` section
- **Features**: Modify `<div class="features-grid">` cards
- **Documentation**: Update code examples in `<section id="docs">`

---

## 🔒 Security

### For Production Deployment:

1. **HTTPS**: GitHub Pages, Netlify, Vercel all provide free SSL
2. **Content Security Policy**: Add to `index.html` `<head>`:

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self';">
```

3. **Permissions Policy**: Add to prevent unwanted features:

```html
<meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=()">
```

---

## 📊 Analytics (Optional)

### Google Analytics

Add before `</head>` in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Plausible Analytics (Privacy-friendly)

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

---

## 🐛 Troubleshooting

### Site Not Loading on GitHub Pages

1. Check repository settings → Pages
2. Ensure `/docs` folder is selected
3. Wait 5 minutes after pushing changes
4. Check for build errors in Actions tab

### CSS/JS Not Loading

1. Verify file paths are relative (not absolute)
2. Check browser console for errors (F12)
3. Clear browser cache (Ctrl+Shift+R)

### Demo Not Working

The demo is a static placeholder. To make it functional:
1. Deploy the backend API server
2. Update API_URL in `script.js`
3. Enable CORS on the server

---

## 📚 Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Netlify Docs](https://docs.netlify.com/)
- [Vercel Docs](https://vercel.com/docs)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## ✅ Deployment Checklist

- [ ] Test website locally
- [ ] Update all GitHub repository links
- [ ] Verify responsive design on mobile
- [ ] Check browser console for errors
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Enable GitHub Pages
- [ ] Test live site
- [ ] (Optional) Configure custom domain
- [ ] (Optional) Add analytics
- [ ] (Optional) Connect to live API backend

---

**Need Help?**  
Contact: datasci@brac.net
