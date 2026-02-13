# Lab Scanner - Installation & Quick Start Guide

## 📦 Installation

### Automatic Installation (Recommended)

1. **Open a terminal** and run:
```bash
bash ~/Desktop/scanner2/INSTALLER.sh
```

2. **Follow the on-screen prompts** - the installer will:
   - Check system requirements (Python 3.8+)
   - Install dependencies into a virtual environment
   - Create desktop shortcuts
   - Set up CLI commands
   - Initialize the database

3. **Wait for completion** - Takes 2-3 minutes depending on internet speed

### What Gets Installed

- **Location**: `~/.local/share/lab-scanner/`
- **CLI Command**: `lab-scanner` (available in any terminal after restarting)
- **Desktop Shortcut**: `~/Desktop/Lab Scanner.desktop` (double-click to launch)
- **Logs**: `/tmp/lab-scanner-*.log` (for debugging)

---

## 🚀 Launching Lab Scanner

You have 3 ways to start Lab Scanner:

### Method 1: Desktop Shortcut (Easiest)
1. Find **"Lab Scanner"** on your desktop
2. Double-click it
3. Dashboard opens automatically in your browser

### Method 2: Terminal Command (Fastest)
```bash
lab-scanner
```
This works from any terminal after installation.

### Method 3: Direct Script
```bash
bash ~/.local/share/lab-scanner/launcher.sh
```

---

## 🌐 Using Lab Scanner Dashboard

Once launched, the dashboard opens at: **http://localhost:5000**

### Network Discovery (Discover Active Hosts)
1. Enter a **CIDR network range** (e.g., `192.168.1.0/24`)
   - `/24` = 256 hosts
   - `/16` = 65,536 hosts
   - Adjust based on your network size
2. Set **thread count** (1-200, default 50)
   - Higher = faster but more network load
3. Click **"🔍 DISCOVER ACTIVE HOSTS"**
4. Results show as clickable boxes

### Individual Host Scanning
1. Click a discovered host OR enter an IP manually
2. Select **scan type**:
   - **Full Scan** (recommended) - comprehensive analysis
   - Port Scan - open ports only
   - Service Detection - identify services
   - Web Scan - web vulnerabilities
3. Click **"🔍 START FULL SCAN"**
4. Results display with:
   - Open ports
   - Services & banners
   - Vulnerabilities (sorted by severity)
   - CVSS risk scores

### API Documentation
Advanced users can access the API docs at: **http://localhost:8000/api/docs**

---

## ⚙️ Configuration

### Modify Settings
Edit `~/.local/share/lab-scanner/app/config.py` to customize:
- API host/port
- Default timeouts
- Thread counts
- Database settings

### Restart After Changes
```bash
# Kill current instance
pkill -f "python -m app.main"
pkill -f "dashboard/app.py"

# Start fresh
lab-scanner
```

---

## 🛠️ Advanced Usage

### Command-Line Options
```bash
# Start just the API
cd ~/.local/share/lab-scanner && \
  source venv/bin/activate && \
  python -m app.main

# Start just the Dashboard
cd ~/.local/share/lab-scanner && \
  source venv/bin/activate && \
  python dashboard/app.py

# Run tests
cd ~/.local/share/lab-scanner && \
  source venv/bin/activate && \
  python -m pytest tests/

# Run interactive demo
cd ~/.local/share/lab-scanner && \
  source venv/bin/activate && \
  python demo.py
```

### View Logs
```bash
# API server logs
tail -f /tmp/lab-scanner-api.log

# Dashboard logs
tail -f /tmp/lab-scanner-dashboard.log
```

### Stop All Services
```bash
# Using pkill
pkill -f "python -m app.main"
pkill -f "dashboard/app.py"

# Or press Ctrl+C in the launcher window
```

---

## 📋 System Requirements

- **OS**: Linux (Kali, Ubuntu, Debian, etc.) or macOS
- **Python**: 3.8 or later
- **pip3**: Package manager (installed with Python)
- **Browser**: Any modern browser (Chrome, Firefox, etc.)
- **RAM**: 512MB minimum (1GB+ recommended)
- **Disk**: 500MB for installation + dependencies

### Install Python (if missing)
```bash
# Kali Linux / Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Ubuntu
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3
```

---

## 🐛 Troubleshooting

### "API OFFLINE" in Dashboard
- Check if API started: `curl http://localhost:8000/api/health`
- Check logs: `tail -20 /tmp/lab-scanner-api.log`
- Try restarting: `lab-scanner`

### Port Already in Use
```bash
# Kill processes on ports 5000 and 8000
sudo lsof -i :5000 -sSUDP -t | xargs kill -9
sudo lsof -i :8000 -sSUDP -t | xargs kill -9
```

### Virtual Environment Issues
```bash
# Reinstall from scratch
rm -rf ~/.local/share/lab-scanner
bash ~/Desktop/scanner2/INSTALLER.sh
```

### Database Errors
```bash
# Reinitialize database
cd ~/.local/share/lab-scanner && \
  source venv/bin/activate && \
  rm lab_scanner.db && \
  python -c "from app.db.database import init_db; init_db()"
```

---

## 📊 Features Overview

✅ **Multi-threaded Port Scanning**
  - 100+ concurrent threads
  - TCP connect method
  - Configurable port ranges

✅ **Service Detection**
  - Banner grabbing
  - Service identification
  - OS fingerprinting

✅ **Web Vulnerability Scanning**
  - Security header checks
  - SSL/TLS validation
  - SQL error detection
  - HTTP method analysis

✅ **Network Discovery**
  - CIDR range scanning
  - Host enumeration
  - Parallel probing

✅ **Vulnerability Assessment**
  - CVSS-style scoring
  - Risk categorization
  - Sorted by severity

✅ **Matrix-Themed Dark UI**
  - Neon cyberpunk aesthetics
  - Color-coded results
  - Responsive design

---

## 📚 More Information

- **Project Location**: `~/Desktop/scanner2/lab_scanner/`
- **Installation Dir**: `~/.local/share/lab-scanner/`
- **API Endpoint**: `http://localhost:8000/api`
- **Dashboard**: `http://localhost:5000`

---

## 🤝 Support

If you encounter issues:
. go to terminal
`/
cd 'Lab Scanner.desktop'
sudo chmod +x 'Lab Scanner.desktop' 
nano ~/Desktop/'Lab scanner.desktop' 
[Desktop Entry]
Name=Lab Scanner
Comment=Launch Lab Scanner
Exec=/home/hons/Desktop/launch-lab-scanner.sh
Icon=/home/hons/Desktop/scanner2/icon.png
Terminal=true
Type=Application
Categories=Utility;
lab-scanner-*.log`
save and exit or try:

1. Check the logs in `/tmp/lab-scanner-*.log`
2. Ensure Python 3.8+ is installed
3. Try reinstalling: `bash ~/Desktop/scanner2/INSTALLER.sh`
4. Check that ports 5000 and 8000 are free

---

**Lab Scanner v1.0** - Professional Vulnerability Scanner
Happy Scanning! 🔍
