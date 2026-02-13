"""
Sample Plugin Template
Use as template for creating new plugins
"""
from typing import Dict
from .base_plugin import BasePlugin


class SamplePlugin(BasePlugin):
    """Sample plugin template for custom checks"""
    
    name = "Sample Plugin"
    description = "Template for creating custom vulnerability checks"
    version = "1.0.0"
    severity = "Info"

    def run(self, target: str, port: int, service: str = "") -> Dict:
        """
        Execute custom check
        
        Args:
            target: Target hostname/IP
            port: Target port
            service: Service name
            
        Returns:
            Dict: Check results
        """
        result = {
            "plugin": self.name,
            "target": target,
            "port": port,
            "service": service,
            "status": "Sample check executed",
            "vulnerable": False,
            "details": "This is a template - implement your logic here"
        }
        
        # TODO: Implement your vulnerability check logic here
        
        self.log_result(result)
        return result
