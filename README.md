# 🔍 Lab Scanner - Professional Vulnerability Scanner

**Enterprise-Grade Network & Web Vulnerability Scanner** with nmap/Nikto/Metasploit style scanning capabilities, powered by FastAPI and modern web dashboard.

---

## ✨ Features

✅ **Multi-threaded Port Scanning** - 100+ concurrent threads with TCP connect methodology  
✅ **Service Detection** - Banner grabbing, service identification, OS fingerprinting  
✅ **Web Vulnerability Scanning** - Headers, SSL/TLS, SQL errors, HTTP methods  
✅ **Network Discovery** - CIDR range scanning with host enumeration  
✅ **Vulnerability Assessment** - CVSS-style scoring with risk categorization  
✅ **Matrix-Themed UI** - Dark neon interface with cyberpunk aesthetics  
✅ **RESTful API** - Full REST API with OpenAPI/Swagger documentation  
✅ **Plugin System** - Extensible architecture for custom scanning modules  
✅ **Distributed Agents** - Master-agent architecture for large-scale scanning  

---

## 🚀 Quick Start (3 Steps)

### Step 1: Verify Requirements
```bash
bash ~/Desktop/scanner2/verify.sh
```
This checks for Python 3.8+, pip, and available ports.

### Step 2: Run Installer
```bash
bash ~/Desktop/scanner2/INSTALLER.sh
```
The installer will:
- Create a virtual environment
- Install all dependencies
- Set up desktop shortcuts
- Initialize the database
- Create CLI commands

**Takes 2-3 minutes** (mostly downloading packages)

### Step 3: Launch Scanner
Choose one of three methods:

**Option A: Desktop Shortcut** (Easiest)
- Find **Lab Scanner** on your desktop
- Double-click it
- Dashboard opens automatically

**Option B: Terminal Command**
```bash
lab-scanner
```
Works from any terminal after restarting it.

**Option C: Direct Script**
```bash
bash ~/.local/share/lab-scanner/launcher.sh
```

---

## 📊 Using Lab Scanner

Once running, open your browser to: **http://localhost:5000**

### Discover Active Hosts
1. Enter network range (e.g., `192.168.1.0/24`)
2. Adjust thread count (1-200, faster = more network load)
3. Click **"🔍 DISCOVER ACTIVE HOSTS"**
4. Results show as clickable boxes

### Scan Individual Hosts
1. Click a discovered host OR enter IP manually
2. Select **scan type**:
   - **Full Scan** - comprehensive analysis (recommended)
   - Port Scan - open ports only
   - Service Detection - identify services
   - Web Scan - web vulnerabilities
3. View results with ports, services, and vulnerabilities

---

## 📋 Files in This Package

```
scanner2/
├── INSTALLER.sh              # ← Run this to install
├── LAUNCHER.sh               # ← Run this to start (or use desktop shortcut)
├── Lab-Scanner.desktop       # Desktop shortcut (auto-created on desktop)
├── verify.sh                 # Pre-installation verification
├── QUICKSTART.md             # Detailed quick start guide
├── README.md                 # This file
└── lab_scanner/              # Main project directory
    ├── app/                  # FastAPI backend
    ├── dashboard/            # Flask frontend
    ├── requirements.txt      # Python dependencies
    └── ...
```

---

## 🛠️ Installation Details

### What Gets Installed?

| Item | Location | Purpose |
|------|----------|---------|
| Python venv | `~/.local/share/lab-scanner/venv/` | Isolated Python environment |
| Application | `~/.local/share/lab-scanner/` | Core scanning application |
| CLI command | `~/.local/bin/lab-scanner` | Run from any terminal |
| Desktop shortcut | `~/Desktop/Lab Scanner.desktop` | Click to launch |
| Launcher script | `~/.local/share/lab-scanner/launcher.sh` | Starts both services |

### System Requirements

- **OS**: Linux (Kali, Ubuntu, Debian, CentOS, etc.) or macOS
- **Python**: 3.8 or later
- **pip3**: Package manager
- **RAM**: 512MB minimum (1GB+ recommended)
- **Disk**: 500MB for installation including dependencies
- **Ports**: 5000 (dashboard), 8000 (API)

### Install Python (if missing)

**Kali Linux / Debian / Ubuntu:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

---

## 🌐 Access Points

Once running:

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:5000 | Web UI for scanning |
| API | http://localhost:8000/api | REST API endpoint |
| API Docs | http://localhost:8000/api/docs | Swagger/OpenAPI |
| Health Check | http://localhost:8000/api/health | API status |

---

## 🔧 Advanced Usage

### View Logs
```bash
# Real-time API logs
tail -f /tmp/lab-scanner-api.log

# Real-time Dashboard logs
tail -f /tmp/lab-scanner-dashboard.log
```

### Modify Configuration
Edit: `~/.local/share/lab-scanner/app/config.py`

Then restart:
```bash
pkill -f "python -m app.main"
pkill -f "dashboard/app.py"
lab-scanner  # restart
```

### Uninstall
```bash
rm -rf ~/.local/share/lab-scanner
rm ~/.local/bin/lab-scanner
rm ~/Desktop/Lab\ Scanner.desktop
```

---

## 🐛 Troubleshooting

### "API OFFLINE" Error
```bash
# Check if API is running
curl http://localhost:8000/api/health

# View API errors
tail -20 /tmp/lab-scanner-api.log

# Restart
lab-scanner
```

### Port Already in Use
```bash
# Kill services on ports
sudo lsof -i :5000 -sSUDP -t | xargs kill -9
sudo lsof -i :8000 -sSUDP -t | xargs kill -9
```

### Python/pip Issues
```bash
# If Python 3 not found
which python3

# If pip3 not found
python3 -m pip --version

# Install missing packages
sudo apt install python3-pip python3-venv
```

### Reinstall Everything
```bash
rm -rf ~/.local/share/lab-scanner
bash ~/Desktop/scanner2/INSTALLER.sh
```

---

## 📚 API Examples

### Check API Health
```bash
curl http://localhost:8000/api/health
```

### Start Port Scan
```bash
curl -X POST http://localhost:8000/api/scan/port \
  -H "Content-Type: application/json" \
  -d '{"target":"192.168.1.1","ports":"1-1000"}'
```

### Discover Network Hosts
```bash
curl -X POST http://localhost:8000/api/discover/network \
  -H "Content-Type: application/json" \
  -d '{"network_range":"192.168.1.0/24","threads":50}'
```

See `http://localhost:8000/api/docs` for full API documentation.

---

## 📖 Project Structure

```
lab_scanner/
├── app/
│   ├── core/
│   │   ├── port_scanner.py      # Multi-threaded port scanning
│   │   ├── service_detector.py  # Service identification
│   │   ├── web_scanner.py       # Web vulnerability checks
│   │   ├── vuln_engine.py       # CVSS scoring
│   │   └── network_scanner.py   # CIDR discovery
│   ├── api/
│   │   ├── routes.py            # FastAPI endpoints
│   │   └── schemas.py           # Pydantic models
│   ├── db/
│   │   ├── models.py            # Database models
│   │   └── database.py          # Database setup
│   ├── plugins/                 # Plugin system
│   ├── config.py                # Configuration
│   └── main.py                  # FastAPI app entry
├── dashboard/
│   ├── app.py                   # Flask backend
│   └── templates/index.html     # Web UI
├── agents/                      # Distributed agents
├── tests/                       # Unit tests
└── requirements.txt             # Dependencies
```

---

## 📊 Technology Stack

- **Backend**: FastAPI (Python async web framework)
- **Frontend**: Flask + HTML5/CSS3/JavaScript
- **Database**: SQLAlchemy ORM (SQLite/PostgreSQL compatible)
- **Scanning**: socket, threading, requests, paramiko
- **Analysis**: CVSS-style vulnerability scoring
- **UI Theme**: Dark neon "Matrix" cyberpunk aesthetic

---

## ⚡ Performance Tips

1. **Network Discovery**: 
   - `/24` networks (256 IPs) with 50 threads: ~2-3 minutes
   - `/25` networks (128 IPs) with 50 threads: ~1-2 minutes
   - Increase threads for faster discovery (more network load)

2. **Port Scanning**:
   - 1-1000 ports with 100 threads: ~30-60 seconds
   - Use common ports (1-1024) for faster scans
   - Top ports scanning is fastest

3. **Memory Usage**:
   - Base: ~100-150MB
   - Per scan: +50-100MB
   - Typical: 200-300MB total

---

## 🤝 Getting Help

1. **Check logs**: `/tmp/lab-scanner-*.log`
2. **Run verification**: `bash ~/Desktop/scanner2/verify.sh`
3. **Restart services**: `lab-scanner`
4. **View API docs**: http://localhost:8000/api/docs

---

## 📄 License & Information

**Lab Scanner v1.0** - Professional Vulnerability Scanner
Inspired by: nmap, Nikto, Metasploit

**Ready to scan?** 🚀

```bash
bash ~/Desktop/scanner2/INSTALLER.sh
```

---

**Happy Scanning!** 🔍
