"""
Service and Banner Detection Module
Detects services running on open ports
"""
import socket
import subprocess
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class ServiceDetector:
    """Detect services and grab banners from open ports"""
    
    # Common port to service mappings
    PORT_SERVICE_MAP = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
    }

    def __init__(self, target: str, timeout: int = 3):
        """
        Initialize service detector
        
        Args:
            target: Target IP/hostname
            timeout: Socket timeout in seconds
        """
        self.target = target
        self.timeout = timeout

    def grab_banner(self, port: int, service: str = "") -> Optional[str]:
        """
        Attempt to grab service banner
        
        Args:
            port: Port to connect to
            service: Service name (optional)
            
        Returns:
            str: Banner information or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.target, port))
            
            # Some services send banner on connect
            try:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                if banner:
                    return banner.strip()
            except:
                pass
            
            # Try common banner grab methods
            if port in [80, 8080, 8443]:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                response = sock.recv(2048).decode('utf-8', errors='ignore')
                return response.split('\r\n')[0] if response else None
            
            sock.close()
            
        except Exception as e:
            logger.debug(f"Could not grab banner on {self.target}:{port} - {str(e)}")
        
        return None

    def detect_service(self, port: int) -> Dict:
        """
        Detect service running on port
        
        Args:
            port: Port number
            
        Returns:
            Dict: Service information
        """
        service = self.PORT_SERVICE_MAP.get(port, "Unknown")
        banner = self.grab_banner(port, service)
        
        return {
            "port": port,
            "service": service,
            "banner": banner if banner else "N/A",
            "status": "open"
        }

    def detect_services(self, ports: List[int]) -> List[Dict]:
        """
        Detect services on multiple ports
        
        Args:
            ports: List of open port numbers
            
        Returns:
            List[Dict]: Service information for each port
        """
        services = []
        for port in ports:
            service_info = self.detect_service(port)
            services.append(service_info)
            logger.info(f"Detected {service_info['service']} on port {port}")
        
        return services


class OSFingerprint:
    """Basic OS fingerprinting based on open ports and services"""
    
    SIGNATURES = {
        "Windows": {
            "ports": [445, 3389],
            "services": ["SMB", "RDP"]
        },
        "Linux": {
            "ports": [22],
            "services": ["SSH"]
        },
        "MacOS": {
            "ports": [22],
            "services": ["SSH"]
        }
    }

    @staticmethod
    def fingerprint(services: List[Dict]) -> str:
        """
        Basic OS fingerprinting
        
        Args:
            services: List of detected services
            
        Returns:
            str: Likely operating system
        """
        open_ports = [s['port'] for s in services]
        service_names = [s['service'] for s in services]
        
        # Simple heuristics
        if 445 in open_ports or 3389 in open_ports:
            return "Windows"
        elif 22 in open_ports:
            return "Linux/Unix"
        
        return "Unknown"
