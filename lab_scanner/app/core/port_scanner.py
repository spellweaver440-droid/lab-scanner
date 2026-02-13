"""
Multi-threaded Port Scanner
Core scanning engine for discovering open ports
"""
import socket
import threading
from queue import Queue
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortScanner:
    """High-performance port scanner using TCP connect methodology"""
    
    def __init__(self, target: str, ports: List[int] = None, threads: int = 100, timeout: int = 2):
        """
        Initialize port scanner
        
        Args:
            target: Target IP/hostname
            ports: List of ports to scan (default: common ports 1-1024)
            threads: Number of worker threads
            timeout: Connection timeout in seconds
        """
        self.target = target
        self.ports = ports or list(range(1, 1025))
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []
        self.closed_ports = []
        self.lock = threading.Lock()
        self.results = {}

    def scan_port(self, port: int) -> bool:
        """
        Scan a single port
        
        Args:
            port: Port number to scan
            
        Returns:
            bool: True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    logger.info(f"✓ Port {port} open on {self.target}")
                return True
            else:
                with self.lock:
                    self.closed_ports.append(port)
                return False
                
        except socket.gaierror:
            logger.error(f"Hostname could not be resolved: {self.target}")
            return False
        except socket.error:
            logger.error(f"Could not connect to {self.target}")
            return False

    def run(self) -> Dict:
        """
        Execute multi-threaded port scan
        
        Returns:
            Dict: Scan results
        """
        logger.info(f"Starting scan on {self.target} ({len(self.ports)} ports, {self.threads} threads)")
        
        queue = Queue()
        for port in self.ports:
            queue.put(port)

        def worker():
            while not queue.empty():
                try:
                    port = queue.get_nowait()
                    self.scan_port(port)
                except:
                    break
                finally:
                    queue.task_done()

        threads = []
        for _ in range(min(self.threads, len(self.ports))):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.results = {
            "target": self.target,
            "total_ports_scanned": len(self.ports),
            "open_ports": sorted(self.open_ports),
            "closed_ports": len(self.closed_ports),
            "status": "completed"
        }
        
        logger.info(f"Scan completed: {len(self.open_ports)} open ports found")
        return self.results

    def get_results(self) -> Dict:
        """Get scan results as dictionary"""
        return self.results
