#!/usr/bin/env python3
"""
Quick Demo Script
Run basic scans to test the system
"""
from app.core.port_scanner import PortScanner
from app.core.service_detector import ServiceDetector
from app.core.vuln_engine import VulnerabilityEngine
import json

def demo_port_scan():
    """Demonstrate port scanning"""
    print("\n" + "="*60)
    print("DEMO: Port Scanning")
    print("="*60)
    
    # Scan localhost (change to your target)
    target = "127.0.0.1"
    ports = [22, 80, 443, 3306, 5432, 8080]
    
    print(f"\n🔍 Scanning {target} for ports: {ports}")
    
    scanner = PortScanner(target, ports, threads=10, timeout=1)
    results = scanner.run()
    
    print(f"\n✓ Scan complete!")
    print(f"  Open ports: {results['open_ports']}")
    print(f"  Closed ports: {results['closed_ports']}")

def demo_service_detection():
    """Demonstrate service detection"""
    print("\n" + "="*60)
    print("DEMO: Service Detection")
    print("="*60)
    
    target = "127.0.0.1"
    open_ports = [22, 80]  # Example
    
    print(f"\n🔎 Detecting services on {target}")
    
    detector = ServiceDetector(target)
    services = detector.detect_services(open_ports)
    
    print(f"\n✓ Services detected:")
    for service in services:
        print(f"  Port {service['port']}: {service['service']}")

def demo_vulnerability_analysis():
    """Demonstrate vulnerability analysis"""
    print("\n" + "="*60)
    print("DEMO: Vulnerability Analysis")
    print("="*60)
    
    # Simulated scan data
    scan_data = {
        "target": "192.168.1.1",
        "services": [
            {"port": 21, "service": "FTP", "banner": "vsftpd"},
            {"port": 22, "service": "SSH", "banner": "OpenSSH_7.4"},
            {"port": 445, "service": "SMB", "banner": "Windows"},
            {"port": 3306, "service": "MySQL", "banner": "MySQL 5.7"},
        ]
    }
    
    print(f"\n📊 Analyzing vulnerabilities for {scan_data['target']}")
    
    report = VulnerabilityEngine.generate_report(scan_data)
    
    print(f"\n✓ Vulnerability Report:")
    print(f"  Total vulnerabilities: {report['vulnerability_count']}")
    print(f"  Risk level: {report['overall_risk_level']}")
    print(f"  Average score: {report['average_risk_score']}")
    print(f"  Max score: {report['max_risk_score']}")
    
    print(f"\n  Top vulnerabilities:")
    for vuln in report['vulnerabilities'][:5]:
        print(f"    • [{vuln['severity']}] {vuln['name']} (port {vuln['port']})")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║   Lab Scanner - Quick Demo               ║
    ║   Enterprise Vulnerability Scanner       ║
    ╚══════════════════════════════════════════╝
    """)
    
    demo_port_scan()
    demo_service_detection()
    demo_vulnerability_analysis()
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Start API: python -m app.main")
    print("  2. Open dashboard: http://localhost:5000")
    print("  3. View API docs: http://localhost:8000/api/docs")
    print("\n")
