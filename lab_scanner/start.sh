#!/bin/bash
# Quick start script for lab scanner

set -e

echo "╔══════════════════════════════════════════╗"
echo "║  Lab Scanner - Setup & Start             ║"
echo "╚══════════════════════════════════════════╝"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "💾 Initializing database..."
python3 -c "from app.db.database import init_db; init_db()"

# Show options
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Choose startup option:                  ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "1) Start FastAPI server (port 8000)"
echo "2) Start Flask dashboard (port 5000)"
echo "3) Run demo"
echo "4) Run tests"
echo "5) Start distributed agent"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting FastAPI server..."
        python3 -m app.main
        ;;
    2)
        echo "🚀 Starting Flask dashboard..."
        cd dashboard
        python3 app.py
        ;;
    3)
        echo "🚀 Running demo..."
        python3 demo.py
        ;;
    4)
        echo "🧪 Running tests..."
        pip install -q pytest
        pytest tests/test_core.py -v
        ;;
    5)
        echo "🤖 Starting distributed agent..."
        python3 run_agent.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
