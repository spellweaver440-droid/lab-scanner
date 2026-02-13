"""
Base Plugin Architecture
NSE-style plugin system for extensible scanning
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """Base abstract plugin class for creating vulnerability checks"""
    
    # Plugin metadata
    name: str = "Base Plugin"
    description: str = "Plugin description"
    version: str = "1.0.0"
    author: str = "Lab Scanner"
    severity: str = "Info"  # Info, Low, Medium, High, Critical

    def __init__(self, target: str, timeout: int = 5):
        """
        Initialize plugin
        
        Args:
            target: Target IP/hostname
            timeout: Operation timeout
        """
        self.target = target
        self.timeout = timeout
        self.results = []

    @abstractmethod
    def run(self, target: str, port: int, service: str = "") -> Dict:
        """
        Execute vulnerability check
        
        Args:
            target: Target host
            port: Target port
            service: Service name (optional)
            
        Returns:
            Dict: Check results
        """
        raise NotImplementedError

    def log_result(self, result: Dict):
        """Log plugin result"""
        self.results.append(result)
        logger.info(f"[{self.name}] {result.get('status', 'unknown')}")

    def get_results(self) -> List[Dict]:
        """Get all plugin results"""
        return self.results
