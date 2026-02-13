#!/bin/bash
# Lab Scanner - Pre-Installation Verification Script

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════╗"
echo "║   Lab Scanner - Pre-Installation Verification      ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

PASS=0
FAIL=0

check_requirement() {
    local name=$1
    local command=$2
    
    if command -v $command &> /dev/null; then
        echo -e "${GREEN}✓${NC} $name - $(which $command)"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $name - NOT FOUND"
        ((FAIL++))
    fi
}

check_version() {
    local name=$1
    local cmd=$2
    local min_version=$3
    
    if command -v $cmd &> /dev/null; then
        local version=$($cmd --version 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} $name - $version"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $name - NOT FOUND (required: $min_version)"
        ((FAIL++))
    fi
}

echo ""
echo "🔍 Checking System Requirements:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_version "Python 3" "python3" "3.8+"
check_requirement "pip (package manager)" "pip3"
check_requirement "curl (for API testing)" "curl"
check_requirement "git (for version control)" "git"

echo ""
echo "🔍 Checking Free Ports:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! nc -z localhost 5000 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Port 5000 - Available (Dashboard)"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Port 5000 - In use (Dashboard)"
    ((FAIL++))
fi

if ! nc -z localhost 8000 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Port 8000 - Available (API)"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} Port 8000 - In use (API)"
    ((FAIL++))
fi

echo ""
echo "🔍 Checking Installation Files:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "/home/hons/Desktop/scanner2/INSTALLER.sh" ]; then
    echo -e "${GREEN}✓${NC} INSTALLER.sh found"
    ((PASS++))
else
    echo -e "${RED}✗${NC} INSTALLER.sh NOT found"
    ((FAIL++))
fi

if [ -f "/home/hons/Desktop/scanner2/LAUNCHER.sh" ]; then
    echo -e "${GREEN}✓${NC} LAUNCHER.sh found"
    ((PASS++))
else
    echo -e "${RED}✗${NC} LAUNCHER.sh NOT found"
    ((FAIL++))
fi

if [ -f "/home/hons/Desktop/scanner2/Lab-Scanner.desktop" ]; then
    echo -e "${GREEN}✓${NC} Lab-Scanner.desktop found"
    ((PASS++))
else
    echo -e "${RED}✗${NC} Lab-Scanner.desktop NOT found"
    ((FAIL++))
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo -e "Results: ${GREEN}$PASS Passed${NC}, ${RED}$FAIL Failed${NC}"
echo "═══════════════════════════════════════════════════"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}"
    echo "✓ Your system is ready for installation!"
    echo -e "${NC}"
    echo "Next step: Run the installer"
    echo ""
    echo "  bash /home/hons/Desktop/scanner2/INSTALLER.sh"
    echo ""
    exit 0
else
    echo -e "${YELLOW}"
    echo "⚠ Some requirements are missing."
    echo -e "${NC}"
    echo "Please fix the above issues and try again."
    echo ""
    
    if [ $(uname -s) == "Linux" ]; then
        echo "To install missing requirements on Kali Linux/Ubuntu:"
        echo ""
        echo "  sudo apt update"
        echo "  sudo apt install python3 python3-pip python3-venv"
        echo "  sudo apt install curl git netcat-openbsd"
        echo ""
    fi
    
    exit 1
fi
