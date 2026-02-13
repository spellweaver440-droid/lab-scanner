"""
Network Discovery Module
Scan networks for active hosts
"""
import socket
import threading
import ipaddress
from queue import Queue
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class NetworkScanner:
    """Discover and scan active hosts on a network"""
    
    def __init__(self, network_range: str, threads: int = 50, timeout: int = 1):
        """
        Initialize network scanner
        
        Args:
            network_range: CIDR notation (e.g., 192.168.1.0/24)
            threads: Number of concurrent threads
            timeout: Connection timeout in seconds
        """
        self.network_range = network_range
        self.threads = threads
        self.timeout = timeout
        self.active_hosts = []
        self.lock = threading.Lock()
    
    def check_host_alive(self, ip: str) -> bool:
        """
        Check if host is alive by testing common ports
        
        Args:
            ip: IP address to check
            
        Returns:
            bool: True if host is alive
        """
        common_ports = [22, 80, 443, 3306, 5432, 8080, 443, 22, 25, 53]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((str(ip), port))
                sock.close()
                
                if result == 0:
                    return True
            except:
                pass
        
        return False
    
    def discover_hosts(self) -> List[str]:
        """
        Discover active hosts on network
        
        Returns:
            List[str]: List of active IP addresses
        """
        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            hosts = list(network.hosts())
            
            logger.info(f"Scanning {len(hosts)} hosts on {self.network_range}")
            
            queue = Queue()
            for host in hosts:
                queue.put(host)
            
            def worker():
                while not queue.empty():
                    try:
                        ip = queue.get_nowait()
                        if self.check_host_alive(ip):
                            with self.lock:
                                self.active_hosts.append(str(ip))
                                logger.info(f"Found active host: {ip}")
                    except:
                        break
                    finally:
                        queue.task_done()
            
            threads = []
            for _ in range(min(self.threads, len(hosts))):
                t = threading.Thread(target=worker, daemon=True)
                t.start()
                threads.append(t)
            
            queue.join()
            
            for t in threads:
                t.join(timeout=1)
            
            return sorted(self.active_hosts)
        
        except ValueError as e:
            logger.error(f"Invalid network range: {str(e)}")
            return []
    
    def get_results(self) -> Dict:
        """Get discovery results"""
        return {
            "network": self.network_range,
            "active_hosts": sorted(self.active_hosts),
            "count": len(self.active_hosts)
        }
