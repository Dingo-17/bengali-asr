#!/bin/bash

# Bengali ASR - Complete Deployment Script
# Deploys frontend to GitHub Pages and provides backend deployment instructions

set -e

echo "🚀 Bengali ASR - Complete Deployment"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Step 2: Get GitHub info
echo -e "${BLUE}Step 2: GitHub Repository Setup${NC}"
echo "Enter your GitHub username:"
read GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}Error: GitHub username cannot be empty${NC}"
    exit 1
fi

echo "Enter repository name (default: bengali-asr):"
read REPO_NAME
REPO_NAME=${REPO_NAME:-bengali-asr}

REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME"
PAGES_URL="https://$GITHUB_USER.github.io/$REPO_NAME"

echo ""
echo -e "${YELLOW}Repository URL: $REPO_URL${NC}"
echo -e "${YELLOW}GitHub Pages URL: $PAGES_URL${NC}"
echo ""

# Step 3: Update API URL in frontend
echo -e "${BLUE}Step 3: Configuring API URL${NC}"
echo ""
echo "Where will you deploy the backend API?"
echo "1) Local testing (http://localhost:8000)"
echo "2) Render.com (free hosting)"
echo "3) Railway.app (free hosting)"
echo "4) Custom URL"
echo ""
echo "Enter choice (1-4):"
read API_CHOICE

case $API_CHOICE in
    1)
        API_URL="http://localhost:8000"
        echo -e "${YELLOW}⚠ Warning: Local API only works for testing, not for deployed site${NC}"
        ;;
    2)
        echo "Enter your Render.com API URL (e.g., https://your-app.onrender.com):"
        read API_URL
        ;;
    3)
        echo "Enter your Railway.app API URL (e.g., https://your-app.up.railway.app):"
        read API_URL
        ;;
    4)
        echo "Enter your custom API URL:"
        read API_URL
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}Updating API URL to: $API_URL${NC}"

# Update API URL in script.js
sed -i.bak "s|const API_URL = .*|const API_URL = '$API_URL';|" docs/script.js
rm docs/script.js.bak

echo -e "${GREEN}✓ API URL updated${NC}"
echo ""

# Step 4: Initialize git repository
echo -e "${BLUE}Step 4: Setting up Git repository${NC}"

if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
else
    echo -e "${YELLOW}Git repository already exists${NC}"
fi

# Create .gitignore
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

# Data and Models (too large for GitHub)
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

# IDE
.vscode/
.idea/

# Keep important files
!docs/*.js
!docs/*.css
!docs/*.html
EOF

echo -e "${GREEN}✓ .gitignore created${NC}"
echo ""

# Step 5: Commit and push
echo -e "${BLUE}Step 5: Committing code${NC}"

git add .
git commit -m "Deploy Bengali ASR: Frontend and Backend setup" || echo "No changes to commit"

# Check if remote exists
if git remote | grep -q "origin"; then
    git remote set-url origin "$REPO_URL.git"
else
    git remote add origin "$REPO_URL.git"
fi

echo -e "${GREEN}✓ Code committed${NC}"
echo ""

# Step 6: Push to GitHub
echo -e "${BLUE}Step 6: Pushing to GitHub${NC}"
echo ""
echo "Make sure you have created the repository at:"
echo -e "${YELLOW}https://github.com/new${NC}"
echo ""
echo "Press ENTER when ready to push..."
read

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo -e "${RED}✗ Failed to push. Please check your credentials and repository.${NC}"
    echo ""
    echo "You may need to:"
    echo "1. Create the repository at: https://github.com/new"
    echo "2. Use a Personal Access Token instead of password"
    echo "3. Check repository permissions"
    exit 1
fi

echo ""

# Step 7: Instructions for GitHub Pages
echo -e "${BLUE}Step 7: Enable GitHub Pages${NC}"
echo ""
echo -e "${YELLOW}To enable GitHub Pages:${NC}"
echo "1. Go to: $REPO_URL/settings/pages"
echo "2. Under 'Source', select:"
echo "   - Branch: main"
echo "   - Folder: /docs"
echo "3. Click 'Save'"
echo ""
echo "Your site will be live at:"
echo -e "${GREEN}$PAGES_URL${NC}"
echo ""
echo "Press ENTER when you've enabled GitHub Pages..."
read

# Step 8: Backend deployment instructions
echo ""
echo -e "${BLUE}Step 8: Deploy Backend API${NC}"
echo ""

if [ "$API_CHOICE" = "1" ]; then
    echo -e "${YELLOW}Local Testing Backend:${NC}"
    echo ""
    echo "To start the backend locally:"
    echo ""
    echo "  cd inference"
    echo "  python server.py"
    echo ""
    echo "⚠ Note: This only works for local testing, not for the deployed GitHub Pages site."
    
elif [ "$API_CHOICE" = "2" ]; then
    echo -e "${YELLOW}Deploy to Render.com:${NC}"
    echo ""
    echo "1. Go to: https://dashboard.render.com/"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository: $REPO_URL"
    echo "4. Configure:"
    echo "   - Name: bengali-asr-api"
    echo "   - Environment: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: cd inference && uvicorn server:app --host 0.0.0.0 --port \$PORT"
    echo "   - Plan: Free"
    echo "5. Add environment variable:"
    echo "   MODEL_TYPE=whisper"
    echo "6. Click 'Create Web Service'"
    echo ""
    echo "After deployment, update the API URL in docs/script.js and redeploy frontend."
    
elif [ "$API_CHOICE" = "3" ]; then
    echo -e "${YELLOW}Deploy to Railway.app:${NC}"
    echo ""
    echo "1. Go to: https://railway.app/"
    echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "3. Select your repository: $REPO_URL"
    echo "4. Add these environment variables:"
    echo "   MODEL_TYPE=whisper"
    echo "   PORT=8000"
    echo "5. Railway will auto-deploy"
    echo ""
    echo "After deployment, update the API URL in docs/script.js and redeploy frontend."
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Frontend URL: $PAGES_URL"
echo "API URL: $API_URL"
echo ""
echo "Next steps:"
echo "1. ✅ Frontend deployed to GitHub Pages"
echo "2. 🔄 Deploy backend API (see instructions above)"
echo "3. 🧪 Test the transcription on your live site"
echo ""
echo "For local testing:"
echo "  cd inference && python server.py"
echo ""
echo "For questions: datasci@brac.net"
echo ""
