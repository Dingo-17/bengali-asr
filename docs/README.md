# Bengali ASR Website

This directory contains the static website for the Bengali Dialect Transcription System.

## 📁 Files

- **`index.html`** - Main webpage with all sections (hero, features, demo, docs, contact)
- **`styles.css`** - Complete styling with responsive design for all screen sizes
- **`script.js`** - Interactive features including mobile menu, demo upload, and smooth scrolling
- **`deploy.sh`** - Automated deployment script for GitHub Pages
- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment instructions for all platforms

## 🚀 Quick Start

### View Locally

```bash
cd docs
python3 -m http.server 8080
```

Then open http://localhost:8080 in your browser.

### Deploy to GitHub Pages

Run the automated deployment script:

```bash
cd /Users/digantohaque/python/BracV1
./docs/deploy.sh
```

The script will:
1. Test the site locally
2. Set up git and .gitignore
3. Update repository links
4. Push to GitHub
5. Provide instructions for enabling GitHub Pages

### Manual Deployment

See `DEPLOYMENT_GUIDE.md` for detailed instructions on deploying to:
- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

## ✨ Features

### Current Features
- ✅ Fully responsive design (mobile, tablet, desktop)
- ✅ Modern, clean UI with smooth animations
- ✅ Interactive navigation with hamburger menu
- ✅ Demo section with drag-and-drop file upload
- ✅ Documentation with code examples
- ✅ Contact information and social links
- ✅ Bengali font support (Noto Sans Bengali)
- ✅ Accessible and SEO-friendly

### Demo Functionality

The demo section currently shows a **static placeholder**. To enable live transcription:

1. Deploy the FastAPI backend server (see main README.md)
2. Update the API endpoint in `script.js`:
   ```javascript
   const API_URL = 'https://your-api-server.com/transcribe';
   ```
3. Enable CORS on your backend to allow requests from your website domain

## 🎨 Customization

### Update Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #10b981;
    /* ... etc */
}
```

### Update Content

All content is in `index.html`:
- Hero section: Lines 35-70
- Features: Lines 72-140
- Demo: Lines 142-250
- Documentation: Lines 252-330

### Update Repository Links

The deployment script automatically updates these, or manually find/replace:
```
https://github.com/BRAC/bengali-dialect-transcription
```

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Android)

## 🔧 Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox/grid
- **Vanilla JavaScript** - No frameworks required
- **Font Awesome** - Icons (CDN)
- **Google Fonts** - Noto Sans Bengali for proper Bengali rendering

## 📊 Performance

- ⚡ Fast loading: < 1MB total size
- 🎯 No build step required
- 📦 No dependencies (all CDN resources)
- 🔒 HTTPS ready for all platforms

## 🐛 Known Issues

None currently. Report issues at: datasci@brac.net

## 📚 Next Steps

After deploying the website:

1. **Connect to Live Backend**
   - Deploy the FastAPI server
   - Update API endpoint in `script.js`
   - Test live transcription

2. **Custom Domain (Optional)**
   - Purchase a domain
   - Configure DNS records
   - Update settings in hosting platform

3. **Analytics (Optional)**
   - Add Google Analytics
   - Or use privacy-friendly Plausible

4. **SEO Optimization**
   - Submit to Google Search Console
   - Generate sitemap
   - Add meta tags for social sharing

## 📄 License

MIT License - See main project LICENSE file

## 👥 Contact

BRAC Data Science Team  
Email: datasci@brac.net  
Website: https://www.brac.net

---

**Ready to deploy?** Run `./deploy.sh` or follow `DEPLOYMENT_GUIDE.md`!
