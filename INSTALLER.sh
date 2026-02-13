#!/bin/bash
#
# Lab Scanner - Multi-Platform Installer
# Supports: Linux (including Kali), macOS
#

set -e

INSTALLER_VERSION="1.0"
OS_TYPE=$(uname -s)
INSTALL_PREFIX="${HOME}/.local/share/lab-scanner"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════╗"
    echo "║     Lab Scanner - Professional Installer v$INSTALLER_VERSION      ║"
    echo "╚════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header

# Check if already installed
if [ -d "$INSTALL_PREFIX" ]; then
    print_info "Lab Scanner is already installed at: $INSTALL_PREFIX"
    read -p "Do you want to reinstall? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled."
        exit 0
    fi
    print_info "Removing old installation..."
    rm -rf "$INSTALL_PREFIX"
fi

# Check Python
print_info "Checking system requirements..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi
print_success "pip3 found"

# Create installation directory
print_info "Creating installation directory..."
mkdir -p "$INSTALL_PREFIX"
print_success "Installation directory created: $INSTALL_PREFIX"

# Copy project files
print_info "Copying project files..."
cp -r "$SCRIPT_DIR/lab_scanner"/* "$INSTALL_PREFIX/"
print_success "Project files copied"

# Create virtual environment
print_info "Creating Python virtual environment..."
cd "$INSTALL_PREFIX"
python3 -m venv venv
print_success "Virtual environment created"

# Activate venv and install dependencies
print_info "Installing dependencies (this may take 2-3 minutes)..."
source "$INSTALL_PREFIX/venv/bin/activate"
pip install -q --upgrade pip setuptools wheel 2>/dev/null || true
pip install -q -r "$INSTALL_PREFIX/requirements.txt"
print_success "Dependencies installed"

# Initialize database
print_info "Initializing database..."
cd "$INSTALL_PREFIX"
python3 -c "from app.db.database import init_db; init_db()" 2>/dev/null || true
print_success "Database initialized"

# Create launcher script
print_info "Creating launcher script..."
cat > "$INSTALL_PREFIX/launcher.sh" << 'LAUNCHER_EOF'
#!/bin/bash
# Lab Scanner Launcher
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$INSTALL_DIR/venv/bin/activate"
cd "$INSTALL_DIR"

# Kill any existing services
pkill -f "python -m app.main" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true

# Start services
echo "🚀 Starting Lab Scanner..."
nohup python -m app.main > /tmp/lab-scanner-api.log 2>&1 &
API_PID=$!
nohup python dashboard/app.py > /tmp/lab-scanner-dashboard.log 2>&1 &
DASH_PID=$!

# Wait for services to start
sleep 3

# Check if services are running
if kill -0 $API_PID 2>/dev/null && kill -0 $DASH_PID 2>/dev/null; then
    echo "✓ Lab Scanner is running!"
    echo "  Dashboard: http://localhost:5000"
    echo "  API: http://localhost:8000/api"
    echo "  API Docs: http://localhost:8000/api/docs"
    
    # Try to open in browser
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5000 2>/dev/null &
    elif command -v open &> /dev/null; then
        open http://localhost:5000 2>/dev/null &
    fi
    
    echo ""
    echo "📊 Lab Scanner Dashboard will open in your browser"
    echo "   Press Ctrl+C to stop the services"
    
    # Keep running - both processes will continue in background
    wait
else
    echo "✗ Failed to start Lab Scanner"
    echo "Check logs: /tmp/lab-scanner-*.log"
    exit 1
fi
LAUNCHER_EOF

chmod +x "$INSTALL_PREFIX/launcher.sh"
print_success "Launcher script created"

# Create CLI alias script
print_info "Creating command-line interface..."
mkdir -p "${HOME}/.local/bin"
cat > "${HOME}/.local/bin/lab-scanner" << 'CLI_EOF'
#!/bin/bash
"$HOME/.local/share/lab-scanner/launcher.sh" "$@"
CLI_EOF

chmod +x "${HOME}/.local/bin/lab-scanner"
print_success "Lab Scanner CLI installed to: ${HOME}/.local/bin/lab-scanner"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
    print_warning "~/.local/bin is not in your PATH"
    print_info "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\${HOME}/.local/bin:\$PATH\""
fi

# Create desktop shortcut
print_info "Creating desktop shortcut..."
mkdir -p "${HOME}/Desktop"
cat > "${HOME}/Desktop/Lab Scanner.desktop" << 'DESKTOP_EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Lab Scanner
Comment=Professional Vulnerability Scanner
Exec=bash -c '"$HOME/.local/share/lab-scanner/launcher.sh"'
Icon=network-wired
Terminal=false
Categories=Utility;Security;Network;
StartupNotify=true
StartupWMClass=lab-scanner
EOF

chmod +x "${HOME}/Desktop/Lab Scanner.desktop"
print_success "Desktop shortcut created: ~/Desktop/Lab Scanner.desktop"

# Final instructions
echo ""
print_header
echo -e "${GREEN}"
echo "✓ Lab Scanner installation completed successfully!"
echo -e "${NC}"
echo ""
echo "📍 Installation location: $INSTALL_PREFIX"
echo ""
echo "🚀 You can launch Lab Scanner in multiple ways:"
echo ""
echo "  1. Click the 'Lab Scanner.desktop' shortcut on your desktop"
echo "  2. Run from terminal: lab-scanner"
echo "  3. Run: $INSTALL_PREFIX/launcher.sh"
echo ""
echo "🌐 Once started, open your browser to: http://localhost:5000"
echo ""
echo "📚 Next steps:"
echo "  • Open the Lab Scanner dashboard"
echo "  • Enter a network range (e.g., 192.168.1.0/24) to discover hosts"
echo "  • Click discovered hosts to perform detailed scans"
echo ""
echo "❓ Need help? Check the logs:"
echo "  • API logs: /tmp/lab-scanner-api.log"
echo "  • Dashboard logs: /tmp/lab-scanner-dashboard.log"
echo ""
print_success "Installation complete! You're ready to scan."
echo ""
