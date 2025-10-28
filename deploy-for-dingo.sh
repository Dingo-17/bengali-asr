#!/bin/bash

# ================================================================
# Personalized Deployment Script for Dingo-17
# ================================================================
# This script automates deployment with your GitHub username
# pre-configured. You'll authenticate via GitHub's standard methods.
# ================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Your Configuration
GITHUB_USERNAME="Dingo-17"
REPO_NAME="bengali-asr"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              🚀 BENGALI ASR DEPLOYMENT 🚀                ║
║                                                           ║
║                    For: Dingo-17                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${GREEN}This script will deploy your Bengali ASR system!${NC}\n"
echo "Configuration:"
echo "  GitHub Username: ${GITHUB_USERNAME}"
echo "  Repository Name: ${REPO_NAME}"
echo "  Repository URL:  ${REPO_URL}"
echo ""

read -p "Press Enter to continue or Ctrl+C to cancel..."

# ================================================================
# Step 1: Check if GitHub repo exists
# ================================================================

echo -e "\n${BLUE}Step 1: Checking GitHub repository...${NC}"

if git ls-remote "${REPO_URL}" &>/dev/null; then
    echo -e "${GREEN}✓ Repository exists!${NC}"
    echo ""
    read -p "Repository already exists. Use it? (y/n): " USE_EXISTING
    
    if [[ ! $USE_EXISTING =~ ^[Yy]$ ]]; then
        echo "Please create a new repository manually at:"
        echo "https://github.com/new"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ Repository doesn't exist yet.${NC}"
    echo ""
    echo "Please create it now:"
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: ${REPO_NAME}"
    echo "3. Make it PUBLIC"
    echo "4. Don't initialize with README"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Press Enter after creating the repository..."
fi

# ================================================================
# Step 2: Initialize Git (if needed)
# ================================================================

echo -e "\n${BLUE}Step 2: Setting up Git...${NC}"

if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
else
    echo -e "${GREEN}✓ Git already initialized${NC}"
fi

# Add remote (if not exists)
if ! git remote get-url origin &>/dev/null; then
    git remote add origin "${REPO_URL}"
    echo -e "${GREEN}✓ Remote added${NC}"
else
    # Update remote to use HTTPS
    git remote set-url origin "${REPO_URL}"
    echo -e "${GREEN}✓ Remote updated${NC}"
fi

# ================================================================
# Step 3: Choose Backend Platform
# ================================================================

echo -e "\n${BLUE}Step 3: Choose backend deployment platform${NC}"
echo ""
echo "1) Railway.app (Recommended - Easy, Free tier)"
echo "2) Render.com (Alternative - Free tier)"
echo "3) Local only (Testing)"
echo ""

read -p "Enter choice (1-3): " BACKEND_CHOICE

case $BACKEND_CHOICE in
    1)
        echo ""
        echo -e "${YELLOW}Railway.app Setup:${NC}"
        echo "After this script completes:"
        echo "1. Go to: https://railway.app"
        echo "2. Sign in with GitHub"
        echo "3. New Project → Deploy from GitHub repo"
        echo "4. Select: ${GITHUB_USERNAME}/${REPO_NAME}"
        echo "5. Copy the Railway URL (e.g., https://bengali-asr-production.up.railway.app)"
        echo ""
        read -p "Enter your Railway URL (or press Enter to skip for now): " RAILWAY_URL
        
        if [ -z "$RAILWAY_URL" ]; then
            API_URL="http://localhost:8000"
            echo -e "${YELLOW}Using localhost for now. Update later!${NC}"
        else
            API_URL="${RAILWAY_URL}"
            echo -e "${GREEN}✓ API URL set to: ${API_URL}${NC}"
        fi
        ;;
    2)
        echo ""
        read -p "Enter your Render.com URL (or press Enter for localhost): " RENDER_URL
        API_URL="${RENDER_URL:-http://localhost:8000}"
        ;;
    3)
        API_URL="http://localhost:8000"
        echo -e "${YELLOW}Using localhost${NC}"
        ;;
esac

# ================================================================
# Step 4: Update Frontend API URL
# ================================================================

echo -e "\n${BLUE}Step 4: Updating frontend configuration...${NC}"

if [ -f "docs/script.js" ]; then
    # Create backup
    cp docs/script.js docs/script.js.backup
    
    # Update API URL
    sed -i '' "s|const API_URL = '.*';|const API_URL = '${API_URL}';|g" docs/script.js
    
    echo -e "${GREEN}✓ API URL updated in script.js${NC}"
    echo "  New URL: ${API_URL}"
else
    echo -e "${RED}✗ script.js not found!${NC}"
    exit 1
fi

# ================================================================
# Step 5: Create .gitignore (if needed)
# ================================================================

echo -e "\n${BLUE}Step 5: Setting up .gitignore...${NC}"

if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'GITIGNORE_EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Models (too large for git)
models/
*.pt
*.pth
*.bin
*.onnx

# Data
data/raw/
data/processed/
*.csv
*.wav
*.mp3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Environment
.env
.env.local

# Backups
*.backup
*.bak
GITIGNORE_EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
else
    echo -e "${GREEN}✓ .gitignore already exists${NC}"
fi

# ================================================================
# Step 6: Commit Changes
# ================================================================

echo -e "\n${BLUE}Step 6: Committing changes...${NC}"

git add .

if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    git commit -m "🚀 Deploy Bengali ASR system - API URL: ${API_URL}"
    echo -e "${GREEN}✓ Changes committed${NC}"
fi

# ================================================================
# Step 7: Push to GitHub
# ================================================================

echo -e "\n${BLUE}Step 7: Pushing to GitHub...${NC}"
echo ""
echo -e "${YELLOW}You'll need to authenticate with GitHub.${NC}"
echo "Options:"
echo "1. Use GitHub CLI (gh auth login)"
echo "2. Use Personal Access Token"
echo "3. Use SSH key"
echo ""
echo "Pushing now..."
echo ""

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Create main branch if needed
if [ "$CURRENT_BRANCH" != "main" ]; then
    git branch -M main
    CURRENT_BRANCH="main"
fi

# Push to GitHub
if git push -u origin main 2>&1 | tee /tmp/git_push_output.txt; then
    echo -e "\n${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo -e "\n${RED}✗ Push failed${NC}"
    echo ""
    echo "Common solutions:"
    echo ""
    echo "1. Use Personal Access Token:"
    echo "   - Go to: https://github.com/settings/tokens"
    echo "   - Generate new token (classic)"
    echo "   - Select 'repo' scope"
    echo "   - Use token as password when prompted"
    echo ""
    echo "2. Use GitHub CLI:"
    echo "   brew install gh"
    echo "   gh auth login"
    echo "   git push -u origin main"
    echo ""
    echo "3. Use SSH:"
    echo "   - Set up SSH key: https://docs.github.com/en/authentication"
    echo "   - Change remote: git remote set-url origin git@github.com:${GITHUB_USERNAME}/${REPO_NAME}.git"
    echo ""
    exit 1
fi

# ================================================================
# Step 8: Instructions for GitHub Pages
# ================================================================

echo -e "\n${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}      Deployment Script Complete! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}\n"

echo -e "${BLUE}Next Steps:${NC}\n"

echo "1. ${YELLOW}Enable GitHub Pages:${NC}"
echo "   a. Go to: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/settings/pages"
echo "   b. Under 'Source':"
echo "      - Branch: main"
echo "      - Folder: /docs"
echo "   c. Click 'Save'"
echo "   d. Wait 2-3 minutes"
echo ""

if [[ $API_URL == "http://localhost:8000" ]]; then
    echo "2. ${YELLOW}Deploy Backend:${NC}"
    echo "   a. Go to: https://railway.app"
    echo "   b. Sign in with GitHub"
    echo "   c. New Project → Deploy from GitHub repo"
    echo "   d. Select: ${GITHUB_USERNAME}/${REPO_NAME}"
    echo "   e. Copy the Railway URL"
    echo ""
    echo "3. ${YELLOW}Update Frontend API URL:${NC}"
    echo "   - Edit docs/script.js line 2"
    echo "   - Change to your Railway URL"
    echo "   - Run: git add . && git commit -m 'Update API URL' && git push"
    echo ""
fi

echo "Your Site URLs:"
echo "  Frontend: ${GREEN}https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/${NC}"
if [[ $API_URL != "http://localhost:8000" ]]; then
    echo "  Backend:  ${GREEN}${API_URL}${NC}"
fi
echo ""

echo -e "${BLUE}Testing:${NC}"
echo "  Backend health: curl ${API_URL}/health"
echo "  Frontend test:  Open docs/test-connection.html"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}For detailed help, see GETTING_STARTED.md${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
