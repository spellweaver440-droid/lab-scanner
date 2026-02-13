"""
Lab Scanner - Comprehensive README
Enterprise-style Vulnerability Scanner
"""

# Lab Scanner - Enterprise Vulnerability Scanner

Professional vulnerability scanner inspired by Nmap, Nikto, and Metasploit.

## 🎯 Features

### Phase 1 - Core Scanner Engine ✅
- **Multi-threaded TCP connect scan** - High-performance port scanning
- **Banner grabbing** - Service version detection
- **Service detection** - Map ports to services
- **JSON reporting** - Structured output format

### Phase 2 - Web Vulnerability Module ✅
- Missing security headers detection
- SQL injection error detection
- HTTP method testing (PUT, DELETE, TRACE)
- SSL/TLS certificate inspection
- Directory discovery (extensible)

### Phase 3 - Plugin System ✅
- NSE-style plugin architecture
- Dynamic plugin loading
- Example plugins: FTP Anonymous, Weak Headers
- Easy plugin creation with BasePlugin class

### Phase 4 - Distributed Agents ✅
- Master-agent architecture
- Task polling mechanism
- Multi-node scanning
- Result aggregation

### Phase 5 - Professional Tool ✅
- CVSS-style simplified risk scoring
- PostgreSQL/SQLite database
- Web dashboard (Flask)
- REST API (FastAPI)
- Docker support
- Comprehensive logging

## 📋 Project Structure

    lab_scanner/
    ├── app/
    │   ├── main.py              # FastAPI entry point
    │   ├── config.py            # Configuration
    │   │
    │   ├── core/
    │   │   ├── port_scanner.py  # Core scanning engine
    │   │   ├── service_detector.py  # Service detection
    │   │   ├── web_scanner.py   # Web vulnerability checks
    │   │   └── vuln_engine.py   # Risk analysis
    │   │
    │   ├── plugins/
    │   │   ├── base_plugin.py   # Plugin base class
    │   │   ├── ftp_anonymous.py # FTP checker
    │   │   ├── weak_headers.py  # Header checker
    │   │   ├── plugin_manager.py # Plugin loader
    │   │   └── sample_plugin.py # Template
    │   │
    │   ├── api/
    │   │   ├── routes.py        # REST endpoints
    │   │   └── schemas.py       # Pydantic models
    │   │
    │   └── db/
    │       ├── models.py        # SQLAlchemy models
    │       └── database.py      # Database setup
    │
    ├── agents/
    │   └── agent.py             # Distributed agent
    │
    ├── dashboard/
    │   ├── app.py               # Flask web UI
    │   └── templates/
    │       └── index.html       # Dashboard interface
    │
    ├── tests/
    │   └── test_core.py         # Unit tests
    │
    ├── requirements.txt         # Python dependencies
    ├── Dockerfile              # API container
    ├── Dockerfile.dashboard    # Dashboard container
    ├── docker-compose.yml      # Multi-container setup
    └── README.md               # This file

## 🚀 Quick Start

### Option 1: Local Installation

1. **Install dependencies:**
   ```bash
   cd lab_scanner
   pip install -r requirements.txt
   ```

2. **Run FastAPI server:**
   ```bash
   python -m app.main
   ```

3. **Run Flask dashboard:**
   ```bash
   cd dashboard
   python app.py
   ```

4. **Access:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/api/docs
   - Dashboard: http://localhost:5000

### Option 2: Docker (Recommended)

1. **Start services:**
   ```bash
   docker-compose up
   ```

2. **Access:**
   - API: http://localhost:8000
   - Dashboard: http://localhost:5000
   - Database: localhost:5432

## 📡 API Endpoints

### Scanning

```bash
# Port scan
POST /api/scan/port
{
  "target": "192.168.1.1",
  "ports": "1-1024",
  "threads": 100,
  "timeout": 2
}

# Full vulnerability scan
POST /api/scan/full
{
  "target": "192.168.1.1",
  "scan_type": "full"
}

# Service detection
GET /api/scan/services?target=192.168.1.1&ports=22,80,443

# Web vulnerability scan
GET /api/scan/web?target=example.com&port=80
```

### Plugin Management

```bash
# List plugins
GET /api/plugins/list

# Run specific plugin
POST /api/plugins/run?plugin_name=FTPAnonymousPlugin&target=192.168.1.1&port=21
```

### Health & Status

```bash
# Health check
GET /api/health

# API status
GET /api/status
```

## 🔌 Creating Custom Plugins

```python
from app.plugins.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    name = "My Security Check"
    description = "Check for specific vulnerability"
    severity = "High"
    
    def run(self, target, port, service=""):
        result = {
            "plugin": self.name,
            "target": target,
            "port": port,
            "vulnerable": False,
            "status": "Check result"
        }
        
        # Your scanning logic here
        # check_result = your_check(target, port)
        # result["vulnerable"] = check_result
        
        self.log_result(result)
        return result
```

Place in `app/plugins/` and PluginManager will auto-load it!

## 📊 Scan Report Example

```json
{
  "target": "192.168.1.10",
  "scan_type": "full",
  "status": "completed",
  "open_ports": [22, 80, 443],
  "services": [
    {
      "port": 22,
      "service": "SSH",
      "banner": "OpenSSH_7.4",
      "status": "open"
    }
  ],
  "vulnerabilities": [
    {
      "name": "SSH Service Detected",
      "severity": "Info",
      "description": "SSH service running on port 22",
      "port": 22,
      "score": 0.1
    }
  ],
  "vulnerability_count": 5,
  "overall_risk_level": "Medium",
  "average_risk_score": 4.5,
  "max_risk_score": 9.0
}
```

## 🤖 Distributed Agent Usage

```python
from agents.agent import ScanAgent

# Create agent
agent = ScanAgent("agent-01", master_url="http://localhost:8000")

# Start polling for tasks
agent.start_polling(poll_interval=5)
```

## 📈 CVSS Risk Scoring

| Severity | Score |
|----------|-------|
| Critical | 9.0   |
| High     | 7.0   |
| Medium   | 5.0   |
| Low      | 3.0   |
| Info     | 0.1   |

## 🧪 Running Tests

```bash
pytest tests/test_core.py -v
```

## 🔧 Configuration

Edit `app/config.py` or set environment variables:

```bash
DATABASE_URL=postgresql://user:pass@localhost/db
LOG_LEVEL=INFO
DEFAULT_THREADS=100
DEFAULT_TIMEOUT=2
```

## 📚 Architecture Overview

```
┌─────────────────────┐
│   FlaskDashboard    │  Web UI
└──────────┬──────────┘
           │ REST
┌──────────▼──────────┐
│   FastAPI Backend   │  REST API
└─────┬────────┬──────┘
      │        │
    ┌─▼─┐   ┌─▼──────────────┐
    │   │   │                │
    ▼   ▼   ▼                ▼
  Port  Web Plugins    Vulnerability
Scan   Scan           Engine
    │   │   │          │
    └─┬─┴─┬─┴──────────┘
      │   │
      ▼   ▼
    PostgreSQL
    SQLite
```

## 🎓 Learning Path

1. **Understand core scanning** → `app/core/port_scanner.py`
2. **Add service detection** → `app/core/service_detector.py`
3. **Create custom checks** → `app/core/` modules
4. **Build plugins** → `app/plugins/`
5. **Extend API** → `app/api/routes.py`
6. **Deploy distributed** → `agents/agent.py`

## 🔐 Security Considerations

⚠️ **For Lab/Educational Use Only**

- Only scan networks you own or have permission to test
- Intensive scanning may impact network performance
- Use timeout and thread limits appropriately
- Store sensitive results securely
- Database should use strong credentials in production

## 📜 Resume Bullet Points

- Designed and built a modular vulnerability scanner inspired by Nmap and Nikto
- Implemented multi-threaded TCP scanning engine with 100+ concurrent threads
- Developed plugin-based architecture for extensible vulnerability checks (NSE-style)
- Built distributed agent-based scanning system with master-agent coordination
- Created REST API using FastAPI with comprehensive JSON reporting
- Containerized application using Docker and Docker Compose for multi-service deployment
- Implemented CVSS-style risk scoring and vulnerability prioritization
- Built responsive web dashboard using Flask and HTML5
- Designed SQLAlchemy ORM models for vulnerability tracking and reporting

## 🤝 Contributing

Contributions welcome! Create new plugins, add features, or improve existing code.

## 📄 License

Lab version for educational purposes

## 🔗 Related Tools

- **Nmap** - Industry standard port scanner
- **Nikto** - Web server scanner
- **Metasploit** - Exploitation framework
- **OpenVAS** - Enterprise vulnerability management
- **ZAP** - Web security testing

## ⭐ Next Steps

1. Test locally with development database
2. Create custom plugins for your lab environment
3. Deploy with PostgreSQL for multi-user support
4. Set up distributed agents on lab VMs
5. Integrate with SIEM/monitoring systems
6. Build dashboard visualizations

---

**Happy scanning! 🔍**

For issues or questions, check the code comments and API docs at `/api/docs`
