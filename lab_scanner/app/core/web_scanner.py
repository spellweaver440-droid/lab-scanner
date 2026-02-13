"""
Web Vulnerability Scanner (Phase 2)
Detects common web vulnerabilities
"""
import requests
import socket
import ssl
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WebScanner:
    """Scan web servers for common vulnerabilities"""
    
    SECURITY_HEADERS = [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Content-Security-Policy",
    ]

    def __init__(self, target: str, timeout: int = 5):
        """
        Initialize web scanner
        
        Args:
            target: Target URL or hostname
            timeout: Request timeout
        """
        self.target = target.rstrip('/')
        self.timeout = timeout
        self.vulns = []

    def check_security_headers(self) -> Dict:
        """Check for missing security headers"""
        missing = []
        try:
            response = requests.head(f"http://{self.target}", 
                                    timeout=self.timeout,
                                    allow_redirects=True)
            
            headers = response.headers
            for header in self.SECURITY_HEADERS:
                if header not in headers:
                    missing.append(header)
            
            return {
                "check": "Missing Security Headers",
                "severity": "Medium",
                "missing_headers": missing,
                "status": "vulnerable" if missing else "safe"
            }
        except Exception as e:
            logger.error(f"Header check failed: {str(e)}")
            return {"check": "Missing Security Headers", "status": "error"}

    def check_ssl_certificate(self) -> Dict:
        """Check SSL certificate validity"""
        try:
            context = ssl.create_default_context()
            conn = socket.create_connection((self.target, 443), timeout=self.timeout)
            ssock = context.wrap_socket(conn, server_hostname=self.target)
            cert = ssock.getpeercert()
            ssock.close()
            
            not_after = cert.get('notAfter', 'Unknown')
            return {
                "check": "SSL Certificate",
                "expiry": not_after,
                "status": "valid"
            }
        except Exception as e:
            return {
                "check": "SSL Certificate",
                "status": "error",
                "error": str(e)
            }

    def check_sql_errors(self) -> Dict:
        """Test for SQL injection error messages"""
        payloads = ["'", "\" OR \"1\"=\"1", "admin' --", "1' UNION SELECT NULL --"]
        vulnerabilities = []
        
        try:
            for payload in payloads:
                try:
                    resp = requests.get(f"http://{self.target}/search",
                                      params={"q": payload},
                                      timeout=self.timeout)
                    
                    error_keywords = ["sql", "mysql", "postgres", "error", "syntax"]
                    if any(keyword in resp.text.lower() for keyword in error_keywords):
                        vulnerabilities.append(payload)
                except:
                    pass
            
            return {
                "check": "SQL Error Detection",
                "severity": "High" if vulnerabilities else "Low",
                "vulnerable": len(vulnerabilities) > 0,
                "payloads": vulnerabilities
            }
        except Exception as e:
            return {"check": "SQL Error Detection", "status": "error"}

    def check_http_methods(self) -> Dict:
        """Test for dangerous HTTP methods"""
        dangerous_methods = []
        
        try:
            for method in ["PUT", "DELETE", "TRACE"]:
                response = requests.request(method, f"http://{self.target}/",
                                          timeout=self.timeout)
                
                if response.status_code < 405:
                    dangerous_methods.append(method)
            
            return {
                "check": "HTTP Methods",
                "severity": "Medium" if dangerous_methods else "Low",
                "allowed_methods": dangerous_methods,
                "status": "vulnerable" if dangerous_methods else "safe"
            }
        except:
            return {"check": "HTTP Methods", "status": "error"}

    def scan(self) -> List[Dict]:
        """Run all web vulnerability checks"""
        logger.info(f"Starting web vulnerability scan on {self.target}")
        
        results = [
            self.check_security_headers(),
            self.check_ssl_certificate(),
            self.check_sql_errors(),
            self.check_http_methods(),
        ]
        
        return results
