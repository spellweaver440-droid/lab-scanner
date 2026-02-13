"""
Vulnerability Engine
CVSS-style simplified risk scoring
"""
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CVSSSeverity(str, Enum):
    """CVSS Severity Ratings"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


class VulnerabilityEngine:
    """Analyze vulnerabilities and assign risk scores"""
    
    # Simplified CVSS scoring
    SEVERITY_SCORES = {
        "Critical": 9.0,
        "High": 7.0,
        "Medium": 5.0,
        "Low": 3.0,
        "Info": 0.1,
    }

    @staticmethod
    def calculate_risk_score(severity: str) -> float:
        """Calculate CVSS-style score"""
        return VulnerabilityEngine.SEVERITY_SCORES.get(severity, 0.0)

    @staticmethod
    def identify_vulnerabilities(service: str, port: int, banner: str = "") -> List[Dict]:
        """
        Identify known vulnerabilities for service
        
        Args:
            service: Service name
            port: Port number
            banner: Service banner/version
            
        Returns:
            List[Dict]: Potential vulnerabilities
        """
        vulns = []
        
        # FTP vulnerabilities
        if service.lower() in ["ftp", "vsftpd"]:
            vulns.append({
                "name": "Anonymous FTP Access",
                "severity": "Medium",
                "description": "FTP server may allow anonymous login",
                "port": port,
                "cve": "N/A"
            })
        
        # SSH vulnerabilities
        if service.lower() == "ssh":
            if "OpenSSH" in banner:
                vulns.append({
                    "name": "SSH Service Detected",
                    "severity": "Info",
                    "description": f"SSH service running: {banner[:50]}",
                    "port": port,
                    "cve": "N/A"
                })
        
        # HTTP vulnerabilities
        if service.lower() in ["http", "http-alt"]:
            vulns.append({
                "name": "Unencrypted HTTP",
                "severity": "Medium",
                "description": "Service running on unencrypted HTTP instead of HTTPS",
                "port": port,
                "cve": "N/A"
            })
        
        # SMB vulnerabilities
        if service.lower() == "smb":
            vulns.append({
                "name": "SMB Service Exposed",
                "severity": "High",
                "description": "Windows File Sharing (SMB) is exposed to network",
                "port": port,
                "cve": "N/A"
            })
        
        # RDP vulnerabilities
        if service.lower() == "rdp":
            vulns.append({
                "name": "RDP Service Exposed",
                "severity": "High",
                "description": "Remote Desktop Protocol publicly accessible",
                "port": port,
                "cve": "N/A"
            })
        
        # Database vulnerabilities
        if service.lower() in ["mysql", "postgresql"]:
            vulns.append({
                "name": "Database Service Exposed",
                "severity": "Critical",
                "description": f"{service} database exposed to network",
                "port": port,
                "cve": "N/A"
            })
        
        return vulns

    @staticmethod
    def generate_report(scan_results: Dict) -> Dict:
        """
        Generate comprehensive vulnerability report
        
        Args:
            scan_results: Results from scanner
            
        Returns:
            Dict: Vulnerability report with risk levels
        """
        vulns = []
        risk_score = 0
        
        # Extract vulnerabilities from scan results
        for service in scan_results.get("services", []):
            service_vulns = VulnerabilityEngine.identify_vulnerabilities(
                service.get("service", "Unknown"),
                service.get("port", 0),
                service.get("banner", "")
            )
            
            for vuln in service_vulns:
                vuln["score"] = VulnerabilityEngine.calculate_risk_score(vuln["severity"])
                vulns.append(vuln)
                risk_score += vuln["score"]
        
        # Calculate overall risk level
        avg_risk = risk_score / len(vulns) if vulns else 0
        if avg_risk >= 8:
            overall_risk = "Critical"
        elif avg_risk >= 6:
            overall_risk = "High"
        elif avg_risk >= 4:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"
        
        return {
            "target": scan_results.get("target", "N/A"),
            "vulnerability_count": len(vulns),
            "vulnerabilities": sorted(vulns, key=lambda x: x["score"], reverse=True),
            "overall_risk_level": overall_risk,
            "average_risk_score": round(avg_risk, 2),
            "max_risk_score": round(max([v["score"] for v in vulns], default=0), 2)
        }
