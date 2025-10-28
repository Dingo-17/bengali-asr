#!/bin/bash

# Deploy Bengali ASR Website to GitHub Pages
# This script automates the process of deploying the website

set -e  # Exit on error

echo "🚀 Bengali ASR Website Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "docs" ]; then
    echo -e "${RED}Error: Please run this script from the BracV1 directory${NC}"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore...${NC}"
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
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi

# Test website locally
echo ""
echo -e "${YELLOW}Testing website locally...${NC}"
echo "Starting local server at http://localhost:8080"
echo "Press Ctrl+C when you're done testing"
echo ""

cd docs
python3 -m http.server 8080 &
SERVER_PID=$!

sleep 2
echo ""
echo -e "${GREEN}✓ Server started (PID: $SERVER_PID)${NC}"
echo "Open http://localhost:8080 in your browser to preview the site"
echo ""
echo "Press any key to continue with deployment (or Ctrl+C to cancel)..."
read -n 1 -s

# Stop the server
kill $SERVER_PID 2>/dev/null || true
cd ..

echo ""
echo -e "${YELLOW}Preparing for GitHub deployment...${NC}"

# Get GitHub username
echo ""
echo "Enter your GitHub username:"
read GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}Error: GitHub username cannot be empty${NC}"
    exit 1
fi

# Get repository name
echo ""
echo "Enter repository name (default: bengali-dialect-transcription):"
read REPO_NAME
REPO_NAME=${REPO_NAME:-bengali-dialect-transcription}

# Update repository links in index.html
echo ""
echo -e "${YELLOW}Updating repository links...${NC}"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME"

# Create a temporary backup
cp docs/index.html docs/index.html.backup

# Update links (macOS compatible)
sed -i.bak "s|https://github.com/BRAC/bengali-dialect-transcription|$REPO_URL|g" docs/index.html
rm docs/index.html.bak
echo -e "${GREEN}✓ Repository links updated${NC}"

# Add all files
echo ""
echo -e "${YELLOW}Adding files to git...${NC}"
git add .
echo -e "${GREEN}✓ Files staged${NC}"

# Commit
echo ""
echo "Enter commit message (default: 'Initial commit: Bengali ASR system'):"
read COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Initial commit: Bengali ASR system"}

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Changes committed${NC}"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}Remote 'origin' already exists. Updating...${NC}"
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
else
    echo -e "${YELLOW}Adding remote 'origin'...${NC}"
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi
echo -e "${GREEN}✓ Remote configured${NC}"

# Push to GitHub
echo ""
echo -e "${YELLOW}Pushing to GitHub...${NC}"
echo "You may need to enter your GitHub credentials or token."
echo ""

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
    echo ""
    echo "=========================================="
    echo "🎉 Deployment Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Go to: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "2. Click 'Settings' → 'Pages'"
    echo "3. Under 'Source', select:"
    echo "   - Branch: main"
    echo "   - Folder: /docs"
    echo "4. Click 'Save'"
    echo ""
    echo "Your site will be live in 2-5 minutes at:"
    echo "https://$GITHUB_USER.github.io/$REPO_NAME/"
    echo ""
    echo "=========================================="
else
    echo ""
    echo -e "${RED}Error: Failed to push to GitHub${NC}"
    echo ""
    echo "Possible issues:"
    echo "1. Repository doesn't exist on GitHub - create it first at:"
    echo "   https://github.com/new"
    echo "2. Authentication failed - you may need a Personal Access Token:"
    echo "   https://github.com/settings/tokens"
    echo "3. Permission denied - check repository access"
    echo ""
    echo "Restoring original index.html..."
    mv docs/index.html.backup docs/index.html 2>/dev/null || true
    exit 1
fi

# Clean up backup
rm docs/index.html.backup 2>/dev/null || true

echo ""
echo "For alternative deployment options (Netlify, Vercel, etc.),"
echo "see: docs/DEPLOYMENT_GUIDE.md"
echo ""
