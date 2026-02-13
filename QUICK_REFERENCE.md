# Lab Scanner - Installation & Launcher Quick Reference

## 🚀 TL;DR (Too Long; Didn't Read)

```bash
# Step 1: Install (2-3 minutes)
bash ~/Desktop/scanner2/INSTALLER.sh

# Step 2: Launch Lab Scanner
lab-scanner

# Step 3: Open in browser
→ http://localhost:5000
```

---

## 📦 What You Have

| File | Purpose | Run |
|------|---------|-----|
| **INSTALLER.sh** | Main installer | `bash INSTALLER.sh` |
| **LAUNCHER.sh** | Starts the scanner | `bash LAUNCHER.sh` |
| **Lab-Scanner.desktop** | Desktop shortcut | Double-click on desktop |
| **verify.sh** | Check system ready | `bash verify.sh` |
| **README.md** | Full documentation | Read in editor |
| **QUICKSTART.md** | Quick guide | Read in editor |

---

## 🎯 3 Ways to Play

### Way 1: Desktop Shortcut (Easiest)
1. After installing, look for **"Lab Scanner"** on your desktop
2. Double-click it
3. Dashboard opens automatically in your browser

### Way 2: Terminal Command
```bash
lab-scanner
```
Works from any terminal after installation and restart.

### Way 3: Manual Script
```bash
bash ~/.local/share/lab-scanner/launcher.sh
```

---

## ✅ Installation Checklist

- [ ] Have Python 3.8+ installed? (`python3 --version`)
- [ ] Have pip3? (`pip3 --version`)
- [ ] Ports 5000 & 8000 free? (`ss -tuln | grep -E '5000|8000'`)
- [ ] Ready to install? Run: `bash ~/Desktop/scanner2/INSTALLER.sh`

---

## 🌐 Dashboard URLs

Once running (after `lab-scanner`):

| URL | Purpose |
|-----|---------|
| http://localhost:5000 | Dashboard (start here!) |
| http://localhost:8000/api | REST API |
| http://localhost:8000/api/docs | Interactive API docs |

---

## 🚨 Installed Locations

After installation, files are at:

```
~/.local/share/lab-scanner/          ← Main app
  ├── venv/                          ← Python virtual environment
  ├── app/                           ← FastAPI backend
  ├── dashboard/                     ← Flask frontend
  └── launcher.sh                    ← Launcher script

~/.local/bin/lab-scanner             ← CLI command
~/Desktop/Lab Scanner.desktop        ← Desktop shortcut
```

---

## 🔧 Quick Commands

```bash
# Start Lab Scanner
lab-scanner

# Kill Lab Scanner
pkill -f "python -m app.main"
pkill -f "dashboard/app.py"

# View API logs
tail -f /tmp/lab-scanner-api.log

# View Dashboard logs
tail -f /tmp/lab-scanner-dashboard.log

# Check if running
curl http://localhost:8000/api/health

# Uninstall
rm -rf ~/.local/share/lab-scanner && \
rm ~/.local/bin/lab-scanner && \
rm ~/Desktop/Lab\ Scanner.desktop
```

---

## 🆘 Fix Common Issues

**Port already in use:**
```bash
sudo lsof -i :5000 -sSUDP -t | xargs kill -9
sudo lsof -i :8000 -sSUDP -t | xargs kill -9
```

**API says "OFFLINE":**
```bash
# Restart everything
pkill -f "python -m app"
pkill -f "dashboard"
lab-scanner
```

**Need to reinstall:**
```bash
rm -rf ~/.local/share/lab-scanner
bash ~/Desktop/scanner2/INSTALLER.sh
```

---

## 📊 What Lab Scanner Does

✅ Network discovery (find hosts on your network)  
✅ Port scanning (find open ports - 1-65535)  
✅ Service detection (identify services on ports)  
✅ Web scanning (find web vulnerabilities)  
✅ Vulnerability scoring (CVSS-style ratings)  
✅ Dark matrix-themed dashboard  
✅ REST API for automation  

---

## 💡 Example Workflow

1. **Start Lab Scanner**
   ```bash
   lab-scanner
   ```

2. **Discover Hosts**
   - Go to http://localhost:5000
   - Enter: `192.168.1.0/24`
   - Click "DISCOVER ACTIVE HOSTS"
   - Wait 2-3 minutes

3. **Scan a Host**
   - Click discovered IP
   - Select "Full Scan"
   - Wait for scan to complete
   - View results (ports, services, vulnerabilities)

4. **Stop Lab Scanner**
   - Press Ctrl+C in the launcher terminal
   - Or: `pkill -f "python -m app"`

---

## 📞 Need Help?

1. Check logs: `tail -20 /tmp/lab-scanner-*.log`
2. Verify install: `bash ~/Desktop/scanner2/verify.sh`
3. Read docs: `cat ~/Desktop/scanner2/QUICKSTART.md`
4. Check API: `curl http://localhost:8000/api/health`

---

**Ready?** Run this:
```bash
bash ~/Desktop/scanner2/INSTALLER.sh
```

Then:
```bash
lab-scanner
```

**Happy Scanning!** 🔍
