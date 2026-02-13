#!/bin/bash
#
# Lab Scanner - Quick Launcher
# This script starts the Lab Scanner services and opens the dashboard
#

INSTALL_DIR="$HOME/.local/share/lab-scanner"
VENV_PATH="$INSTALL_DIR/venv"
PID_FILE="/tmp/lab-scanner-pids"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[Lab Scanner]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to cleanup
cleanup() {
    print_status "Shutting down services..."
    if [ -f "$PID_FILE" ]; then
        while IFS= read -r pid; do
            kill "$pid" 2>/dev/null || true
        done < "$PID_FILE"
        rm "$PID_FILE"
    fi
    print_success "Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Check if installed
if [ ! -d "$INSTALL_DIR" ]; then
    print_error "Lab Scanner not installed. Please run the installer first:"
    echo "  bash ~/Desktop/scanner2/INSTALLER.sh"
    exit 1
fi

print_status "Lab Scanner Launcher v1.0"
print_status "=========================="
print_status ""

# Kill any existing processes
print_status "Cleaning up existing processes..."
pkill -f "python -m app.main" 2>/dev/null || true
pkill -f "python.*dashboard/app.py" 2>/dev/null || true
sleep 1

# Source virtual environment
source "$VENV_PATH/bin/activate" 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

cd "$INSTALL_DIR"

# Start API server
print_status "Starting API server on port 8000..."
nohup python -m app.main > /tmp/lab-scanner-api.log 2>&1 &
API_PID=$!
echo "$API_PID" >> "$PID_FILE"

# Start Dashboard
print_status "Starting Dashboard on port 5000..."
nohup python dashboard/app.py > /tmp/lab-scanner-dashboard.log 2>&1 &
DASH_PID=$!
echo "$DASH_PID" >> "$PID_FILE"

# Wait for services to start
print_status "Waiting for services to start..."
sleep 4

# Check if services are running
if kill -0 $API_PID 2>/dev/null && kill -0 $DASH_PID 2>/dev/null; then
    print_success "All services started successfully!"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Lab Scanner is now running!${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "  📊 Dashboard:    http://localhost:5000"
    echo "  🔌 API Endpoint: http://localhost:8000/api"
    echo "  📖 API Docs:     http://localhost:8000/api/docs"
    echo ""
    echo "  Process IDs:"
    echo "    API Server:   $API_PID"
    echo "    Dashboard:    $DASH_PID"
    echo ""
    echo -e "${YELLOW}  To stop services, close this window or press Ctrl+C${NC}"
    echo ""
    
    # Try to open browser
    if command -v xdg-open &> /dev/null; then
        print_status "Opening dashboard in browser..."
        xdg-open http://localhost:5000 2>/dev/null &
    elif command -v firefox &> /dev/null; then
        firefox http://localhost:5000 2>/dev/null &
    elif command -v chromium &> /dev/null; then
        chromium http://localhost:5000 2>/dev/null &
    fi
    
    # Keep the launcher running (for cleanup on exit)
    wait
else
    print_error "Failed to start services"
    echo ""
    echo "Debug information:"
    echo "===================="
    if [ -f /tmp/lab-scanner-api.log ]; then
        echo "API Server log (last 10 lines):"
        tail -10 /tmp/lab-scanner-api.log
    fi
    if [ -f /tmp/lab-scanner-dashboard.log ]; then
        echo ""
        echo "Dashboard log (last 10 lines):"
        tail -10 /tmp/lab-scanner-dashboard.log
    fi
    exit 1
fi
