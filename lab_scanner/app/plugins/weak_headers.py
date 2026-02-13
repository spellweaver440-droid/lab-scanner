"""
Weak Security Headers Detection Plugin
"""
import requests
from typing import Dict
from .base_plugin import BasePlugin


class WeakHeadersPlugin(BasePlugin):
    """Detect missing or weak security headers"""
    
    name = "Weak Security Headers"
    description = "Detects missing or improperly configured security headers"
    version = "1.0.0"
    severity = "Medium"

    SECURITY_HEADERS = {
        "Strict-Transport-Security": "Critical",
        "X-Content-Type-Options": "High",
        "X-Frame-Options": "High",
        "X-XSS-Protection": "Medium",
        "Content-Security-Policy": "High",
    }

    def run(self, target: str, port: int, service: str = "") -> Dict:
        """
        Check for weak security headers
        
        Args:
            target: Target hostname
            port: HTTP/HTTPS port
            service: Service name
            
        Returns:
            Dict: Header analysis results
        """
        result = {
            "plugin": self.name,
            "target": target,
            "port": port,
            "vulnerable": False,
            "missing_headers": [],
            "headers_found": []
        }

        try:
            url = f"http://{target}:{port}" if port != 443 else f"https://{target}:{port}"
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            
            missing = []
            found = []
            
            for header, severity in self.SECURITY_HEADERS.items():
                if header not in response.headers:
                    missing.append({"header": header, "severity": severity})
                else:
                    found.append({"header": header, "value": response.headers[header][:50]})
            
            result["missing_headers"] = missing
            result["headers_found"] = found
            result["vulnerable"] = len(missing) > 0
            result["status"] = f"Found {len(found)}/{len(self.SECURITY_HEADERS)} headers"
            
        except Exception as e:
            result["status"] = f"Error - {str(e)[:50]}"

        self.log_result(result)
        return result
