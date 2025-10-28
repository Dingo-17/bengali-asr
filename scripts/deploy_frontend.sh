#!/bin/bash
# Deploy React frontend to GitHub Pages

set -e

echo "========================================"
echo "Deploying Frontend to GitHub Pages"
echo "========================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    echo "Please run this script from the repository root"
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing dependencies..."
npm install

# Build production bundle
echo "Building production bundle..."
npm run build

# Create gh-pages branch if it doesn't exist
git branch -D gh-pages 2>/dev/null || true
git checkout --orphan gh-pages

# Remove all files except build
git rm -rf . 2>/dev/null || true

# Copy build files to root
cp -r dist/* .

# Create CNAME file if custom domain is configured
# Uncomment and edit if you have a custom domain:
# echo "your-domain.com" > CNAME

# Add .nojekyll file to prevent GitHub from processing with Jekyll
touch .nojekyll

# Commit and push
git add .
git commit -m "Deploy to GitHub Pages"

echo ""
echo "Pushing to gh-pages branch..."
git push -f origin gh-pages

# Return to main branch
git checkout main

echo ""
echo "========================================"
echo "✓ Deployment complete!"
echo "========================================"
echo ""
echo "Your site will be available at:"
echo "  https://<username>.github.io/<repository>"
echo ""
echo "To set up a custom domain:"
echo "  1. Add a CNAME file with your domain"
echo "  2. Configure DNS settings"
echo "  3. Enable HTTPS in repository settings"
echo ""
