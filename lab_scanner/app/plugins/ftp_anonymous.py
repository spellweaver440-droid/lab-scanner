"""
FTP Anonymous Login Detection Plugin
"""
import ftplib
from typing import Dict
from .base_plugin import BasePlugin


class FTPAnonymousPlugin(BasePlugin):
    """Detect FTP servers allowing anonymous logins"""
    
    name = "FTP Anonymous Login"
    description = "Tests for FTP servers allowing anonymous access"
    version = "1.0.0"
    severity = "High"

    def run(self, target: str, port: int, service: str = "") -> Dict:
        """
        Test for anonymous FTP access
        
        Args:
            target: Target hostname/IP
            port: FTP port (usually 21)
            service: Service name
            
        Returns:
            Dict: Test results
        """
        result = {
            "plugin": self.name,
            "target": target,
            "port": port,
            "service": service or "FTP",
            "vulnerable": False,
            "status": "Safe"
        }

        try:
            ftp = ftplib.FTP(timeout=self.timeout)
            ftp.connect(target, port)
            
            # Try anonymous login
            ftp.login('anonymous', 'anonymous@example.com')
            
            # If successful, server is vulnerable
            ftp.quit()
            
            result["vulnerable"] = True
            result["status"] = "Vulnerable - Anonymous login allowed"
            result["severity"] = self.severity
            
        except ftplib.all_errors as e:
            result["status"] = f"Not vulnerable - {str(e)[:50]}"
        except Exception as e:
            result["status"] = f"Could not connect - {str(e)[:50]}"

        self.log_result(result)
        return result
