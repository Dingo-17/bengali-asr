#!/bin/bash

# ================================================================
# 🚀 Bengali ASR - One-Click Setup
# ================================================================
# This script helps you get started quickly with deployment
# ================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# ASCII Art Banner
clear
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗███╗   ██╗ ██████╗  █████╗ ██╗        ║
║   ██╔══██╗██╔════╝████╗  ██║██╔════╝ ██╔══██╗██║        ║
║   ██████╔╝█████╗  ██╔██╗ ██║██║  ███╗███████║██║        ║
║   ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██║        ║
║   ██████╔╝███████╗██║ ╚████║╚██████╔╝██║  ██║███████╗   ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ║
║                                                           ║
║          ASR - Automatic Speech Recognition               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

      Bengali Dialect Transcription System
      Ready for Production Deployment! 🎉

EOF
echo -e "${NC}"

echo -e "${GREEN}Welcome!${NC} This script will help you deploy your system.\n"

# ================================================================
# Main Menu
# ================================================================

echo -e "${BLUE}What would you like to do?${NC}\n"
echo "1) 🚀 Full Deployment (Frontend + Backend)"
echo "2) 🧪 Test Locally First"
echo "3) 📚 View Documentation"
echo "4) 🔧 Configure Settings"
echo "5) ❌ Exit"
echo ""

read -p "Enter your choice (1-5): " CHOICE

case $CHOICE in
    1)
        echo -e "\n${GREEN}Starting Full Deployment...${NC}\n"
        ./deploy-github-pages.sh
        ;;
    2)
        echo -e "\n${GREEN}Setting up local testing environment...${NC}\n"
        
        echo -e "${YELLOW}This will:${NC}"
        echo "1. Start the backend server on http://localhost:8000"
        echo "2. Open the test connection page"
        echo "3. Open the frontend website"
        echo ""
        
        read -p "Continue? (y/n): " CONFIRM
        
        if [[ $CONFIRM == "y" || $CONFIRM == "Y" ]]; then
            echo -e "\n${BLUE}Starting backend server...${NC}"
            echo "Note: This will run in the background."
            echo ""
            
            # Check if server is already running
            if lsof -i :8000 > /dev/null 2>&1; then
                echo -e "${YELLOW}⚠ Port 8000 is already in use.${NC}"
                echo "Would you like to:"
                echo "1) Stop existing server and restart"
                echo "2) Use existing server"
                read -p "Choice (1-2): " SERVER_CHOICE
                
                if [[ $SERVER_CHOICE == "1" ]]; then
                    echo "Stopping existing server..."
                    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
                    sleep 2
                fi
            fi
            
            # Start backend
            cd /Users/digantohaque/python/BracV1
            python -m uvicorn inference.server:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
            BACKEND_PID=$!
            
            echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
            echo "Backend running at: http://localhost:8000"
            echo ""
            
            sleep 3
            
            # Test backend
            echo -e "${BLUE}Testing backend...${NC}"
            if curl -s http://localhost:8000/health > /dev/null; then
                echo -e "${GREEN}✓ Backend is responding!${NC}"
                echo ""
            else
                echo -e "${RED}✗ Backend not responding. Check logs.${NC}"
                echo "You can check logs with: tail -f logs/server.log"
                echo ""
            fi
            
            # Open test page
            echo -e "${BLUE}Opening test connection page...${NC}"
            open file:///Users/digantohaque/python/BracV1/docs/test-connection.html 2>/dev/null || \
            python -c "import webbrowser; webbrowser.open('file:///Users/digantohaque/python/BracV1/docs/test-connection.html')"
            
            sleep 2
            
            # Open frontend
            echo -e "${BLUE}Opening frontend website...${NC}"
            open file:///Users/digantohaque/python/BracV1/docs/index.html 2>/dev/null || \
            python -c "import webbrowser; webbrowser.open('file:///Users/digantohaque/python/BracV1/docs/index.html')"
            
            echo ""
            echo -e "${GREEN}✓ Local testing environment ready!${NC}"
            echo ""
            echo -e "${CYAN}Next steps:${NC}"
            echo "1. Test the connection in the opened browser"
            echo "2. Try uploading an audio file"
            echo "3. When done, stop the backend with:"
            echo "   kill $BACKEND_PID"
            echo ""
            
        else
            echo "Cancelled."
        fi
        ;;
    3)
        echo -e "\n${GREEN}Available Documentation:${NC}\n"
        
        echo -e "${CYAN}Getting Started:${NC}"
        echo "  • DOCUMENTATION_INDEX.md  - Master index of all docs"
        echo "  • GETTING_STARTED.md      - Beginner's guide (20 min)"
        echo "  • QUICKSTART_DEPLOY.md    - Fast deployment (15 min)"
        echo ""
        
        echo -e "${CYAN}Deployment Guides:${NC}"
        echo "  • DEPLOY_GITHUB_PAGES.md  - Detailed deployment guide"
        echo "  • DEPLOYMENT_SUMMARY.md   - Quick overview"
        echo "  • DEPLOYMENT_COMPLETE.md  - Comprehensive guide"
        echo ""
        
        echo -e "${CYAN}Technical Documentation:${NC}"
        echo "  • README.md               - Project overview"
        echo "  • PROJECT_SUMMARY.md      - Technical details"
        echo "  • ARCHITECTURE.md         - System architecture"
        echo "  • TROUBLESHOOTING.md      - Problem solving"
        echo ""
        
        echo -e "${CYAN}Frontend:${NC}"
        echo "  • docs/README.md          - Frontend documentation"
        echo "  • docs/test-connection.html - API testing tool"
        echo ""
        
        read -p "Would you like to open a document? (y/n): " OPEN_DOC
        
        if [[ $OPEN_DOC == "y" || $OPEN_DOC == "Y" ]]; then
            echo ""
            echo "Which document?"
            echo "1) GETTING_STARTED.md (recommended for beginners)"
            echo "2) DOCUMENTATION_INDEX.md (all docs overview)"
            echo "3) QUICKSTART_DEPLOY.md (fast deployment)"
            echo "4) ARCHITECTURE.md (technical architecture)"
            echo ""
            
            read -p "Choice (1-4): " DOC_CHOICE
            
            case $DOC_CHOICE in
                1) open GETTING_STARTED.md 2>/dev/null || cat GETTING_STARTED.md ;;
                2) open DOCUMENTATION_INDEX.md 2>/dev/null || cat DOCUMENTATION_INDEX.md ;;
                3) open QUICKSTART_DEPLOY.md 2>/dev/null || cat QUICKSTART_DEPLOY.md ;;
                4) open ARCHITECTURE.md 2>/dev/null || cat ARCHITECTURE.md ;;
                *) echo "Invalid choice" ;;
            esac
        fi
        ;;
    4)
        echo -e "\n${GREEN}Configuration Settings${NC}\n"
        
        echo -e "${CYAN}Current Configuration:${NC}"
        echo ""
        
        # Check API URL in script.js
        if [ -f "docs/script.js" ]; then
            API_URL=$(grep "const API_URL" docs/script.js | cut -d"'" -f2)
            echo "Frontend API URL: ${YELLOW}$API_URL${NC}"
        fi
        
        echo ""
        echo "What would you like to configure?"
        echo "1) Update Frontend API URL"
        echo "2) View Backend Configuration"
        echo "3) Back to Main Menu"
        echo ""
        
        read -p "Choice (1-3): " CONFIG_CHOICE
        
        case $CONFIG_CHOICE in
            1)
                echo ""
                echo -e "${YELLOW}Enter your new API URL:${NC}"
                echo "Examples:"
                echo "  - http://localhost:8000 (local)"
                echo "  - https://your-app.up.railway.app (Railway)"
                echo "  - https://your-app.onrender.com (Render)"
                echo ""
                
                read -p "API URL: " NEW_API_URL
                
                if [ ! -z "$NEW_API_URL" ]; then
                    sed -i.bak "s|const API_URL = '.*';|const API_URL = '$NEW_API_URL';|g" docs/script.js
                    rm docs/script.js.bak
                    echo -e "${GREEN}✓ API URL updated!${NC}"
                    echo "New URL: $NEW_API_URL"
                else
                    echo "No URL provided. Skipping."
                fi
                ;;
            2)
                echo ""
                echo -e "${CYAN}Backend Configuration Files:${NC}"
                echo "  • railway.toml        - Railway deployment"
                echo "  • render.yaml         - Render deployment"
                echo "  • requirements.txt    - Python dependencies"
                echo "  • inference/server.py - Main server file"
                echo ""
                echo "Model Type: Wav2Vec2 (default)"
                echo "Device: CPU (auto-detected)"
                echo "Max Audio Duration: 60 seconds"
                echo "Max File Size: 10 MB"
                ;;
            3)
                exec "$0"
                ;;
        esac
        ;;
    5)
        echo -e "\n${GREEN}Thank you for using Bengali ASR!${NC}"
        echo -e "${CYAN}For help, check: DOCUMENTATION_INDEX.md${NC}\n"
        exit 0
        ;;
    *)
        echo -e "\n${RED}Invalid choice. Please run again.${NC}\n"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}Done! Need help? Check DOCUMENTATION_INDEX.md${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
