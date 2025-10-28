#!/bin/bash

# ================================================================
# Bengali ASR - GitHub Pages + Railway Deployment Script
# ================================================================
# This script automates deployment of:
# - Frontend to GitHub Pages
# - Backend to Railway.app
# 
# Prerequisites:
# - Git repository initialized
# - GitHub remote added
# - Railway CLI installed (optional, for CLI deployment)
# ================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# ================================================================
# Part 1: Pre-deployment Checks
# ================================================================

print_step "Checking prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi
print_success "Git found"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_warning "Not a git repository. Initializing..."
    git init
    print_success "Git repository initialized"
else
    print_success "Git repository found"
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    print_warning "No git remote found."
    echo -e "${YELLOW}Please enter your GitHub repository URL (e.g., https://github.com/username/repo.git):${NC}"
    read -r REPO_URL
    git remote add origin "$REPO_URL"
    print_success "Git remote added"
else
    REPO_URL=$(git remote get-url origin)
    print_success "Git remote found: $REPO_URL"
fi

# ================================================================
# Part 2: Update API URL
# ================================================================

print_step "Configuring API URL..."

echo -e "${YELLOW}Choose deployment option:${NC}"
echo "1) Railway.app (recommended - free tier)"
echo "2) Render.com (free tier)"
echo "3) Heroku (paid)"
echo "4) Local development (localhost:8000)"
echo "5) Custom URL"

read -p "Enter option (1-5): " DEPLOY_OPTION

case $DEPLOY_OPTION in
    1)
        echo -e "${YELLOW}Enter your Railway app name (e.g., my-bengali-asr):${NC}"
        read -r RAILWAY_APP_NAME
        API_URL="https://${RAILWAY_APP_NAME}.up.railway.app"
        ;;
    2)
        echo -e "${YELLOW}Enter your Render app name (e.g., my-bengali-asr):${NC}"
        read -r RENDER_APP_NAME
        API_URL="https://${RENDER_APP_NAME}.onrender.com"
        ;;
    3)
        echo -e "${YELLOW}Enter your Heroku app name:${NC}"
        read -r HEROKU_APP_NAME
        API_URL="https://${HEROKU_APP_NAME}.herokuapp.com"
        ;;
    4)
        API_URL="http://localhost:8000"
        print_warning "Using localhost - only for development!"
        ;;
    5)
        echo -e "${YELLOW}Enter your custom API URL (e.g., https://api.example.com):${NC}"
        read -r API_URL
        ;;
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

print_success "API URL set to: $API_URL"

# Update script.js
print_step "Updating docs/script.js with API URL..."

if [ -f "docs/script.js" ]; then
    # Create backup
    cp docs/script.js docs/script.js.backup
    
    # Update API_URL
    sed -i.bak "s|const API_URL = '.*';|const API_URL = '$API_URL';|g" docs/script.js
    rm docs/script.js.bak
    
    print_success "API URL updated in script.js"
else
    print_error "docs/script.js not found!"
    exit 1
fi

# ================================================================
# Part 3: Git Commit and Push
# ================================================================

print_step "Committing changes..."

# Add all files
git add .

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    print_warning "No changes to commit"
else
    # Commit
    git commit -m "🚀 Deploy: Update API URL to $API_URL"
    print_success "Changes committed"
fi

# ================================================================
# Part 4: Push to GitHub
# ================================================================

print_step "Pushing to GitHub..."

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push to GitHub
if git push origin "$CURRENT_BRANCH"; then
    print_success "Pushed to GitHub (branch: $CURRENT_BRANCH)"
else
    print_error "Failed to push to GitHub"
    print_warning "You may need to: git push -u origin $CURRENT_BRANCH"
    exit 1
fi

# ================================================================
# Part 5: GitHub Pages Setup Instructions
# ================================================================

print_step "GitHub Pages Setup"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Next Steps:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Go to your GitHub repository:"
echo "   $REPO_URL"
echo ""
echo "2. Click 'Settings' tab"
echo ""
echo "3. Click 'Pages' in the left sidebar"
echo ""
echo "4. Under 'Source':"
echo "   - Branch: ${CURRENT_BRANCH}"
echo "   - Folder: /docs"
echo "   - Click 'Save'"
echo ""
echo "5. Wait 2-3 minutes for deployment"
echo ""
echo "6. Your site will be live at:"

# Extract username and repo from URL
if [[ $REPO_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
    USERNAME="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    PAGES_URL="https://${USERNAME}.github.io/${REPO}/"
    echo "   ${GREEN}${PAGES_URL}${NC}"
else
    echo "   https://[username].github.io/[repo-name]/"
fi

echo ""
echo -e "${GREEN}========================================${NC}"

# ================================================================
# Part 6: Backend Deployment Instructions
# ================================================================

print_step "Backend Deployment"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Backend Deployment:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

case $DEPLOY_OPTION in
    1)
        echo "Railway.app Deployment:"
        echo ""
        echo "Option A - Using Railway Dashboard (Recommended):"
        echo "1. Go to https://railway.app"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Project'"
        echo "4. Select 'Deploy from GitHub repo'"
        echo "5. Choose your repository"
        echo "6. Railway will auto-detect and deploy"
        echo "7. Set environment variables (optional):"
        echo "   MODEL_TYPE=wav2vec2"
        echo "   PYTHON_VERSION=3.10"
        echo ""
        echo "Option B - Using Railway CLI:"
        echo "1. Install: npm i -g @railway/cli"
        echo "2. Login: railway login"
        echo "3. Deploy: railway up"
        ;;
    2)
        echo "Render.com Deployment:"
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New' -> 'Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Configure:"
        echo "   - Name: bengali-asr-api"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn inference.server:app --host 0.0.0.0 --port \$PORT"
        echo "6. Click 'Create Web Service'"
        ;;
    3)
        echo "Heroku Deployment:"
        echo ""
        echo "1. Install Heroku CLI: brew install heroku/brew/heroku"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create your-app-name"
        echo "4. Deploy: git push heroku main"
        echo "5. Open: heroku open"
        ;;
    4)
        echo "Local Development:"
        echo ""
        echo "Terminal 1 - Start Backend:"
        echo "cd /Users/digantohaque/python/BracV1"
        echo "python -m uvicorn inference.server:app --host 0.0.0.0 --port 8000"
        echo ""
        echo "Terminal 2 - Start Frontend:"
        echo "cd /Users/digantohaque/python/BracV1/docs"
        echo "python -m http.server 3000"
        echo ""
        echo "Visit: http://localhost:3000"
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"

# ================================================================
# Part 7: Testing Instructions
# ================================================================

print_step "Testing"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}After Deployment, Test Your System:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Test Backend Health:"
echo "   curl ${API_URL}/health"
echo ""
echo "2. Visit Frontend:"
if [ ! -z "$PAGES_URL" ]; then
    echo "   $PAGES_URL"
else
    echo "   https://[username].github.io/[repo-name]/"
fi
echo ""
echo "3. Try Demo:"
echo "   - Go to 'Try Demo' section"
echo "   - Upload an audio file"
echo "   - Click 'Transcribe'"
echo "   - Verify transcription appears"
echo ""
echo -e "${GREEN}========================================${NC}"

# ================================================================
# Summary
# ================================================================

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Summary:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "✓ Code committed and pushed to GitHub"
echo "✓ API URL updated: $API_URL"
echo "✓ Ready for GitHub Pages deployment"
echo ""
echo "Next Actions:"
echo "1. Enable GitHub Pages (see instructions above)"
echo "2. Deploy backend to $DEPLOY_OPTION"
echo "3. Test end-to-end functionality"
echo ""
echo -e "${GREEN}========================================${NC}"
echo ""
print_success "Deployment script complete! 🚀"
echo ""
echo "Need help? Check DEPLOY_GITHUB_PAGES.md for detailed instructions."
