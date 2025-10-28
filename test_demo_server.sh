#!/bin/bash

echo "🧪 Testing Demo Server Locally..."
echo ""
echo "📦 Installing dependencies..."
pip install -q fastapi uvicorn python-multipart

echo ""
echo "🚀 Starting demo server on port 8000..."
echo "   (Press Ctrl+C to stop)"
echo ""
echo "   Test endpoints:"
echo "   - Health: http://localhost:8000/health"
echo "   - Docs:   http://localhost:8000/docs"
echo ""

cd "$(dirname "$0")"
uvicorn inference.demo_server:app --host 0.0.0.0 --port 8000 --reload
