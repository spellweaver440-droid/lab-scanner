#!/usr/bin/env python3
"""
Network Discovery Scanner
Scan entire network subnets for active hosts and open ports
"""
import socket
import threading
import ipaddress
from queue import Queue
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class NetworkDiscovery:
    """Discover active hosts on a network"""
    
    def __init__(self, network_range, threads=50):
        """
        Initialize network scanner
        
        Args:
            network_range: CIDR notation (e.g., 192.168.1.0/24)
            threads: Number of concurrent threads
        """
        self.network_range = network_range
        self.threads = threads
        self.active_hosts = []
        self.lock = threading.Lock()
    
    def ping_host(self, ip):
        """Check if host is alive using TCP connect on common ports"""
        common_ports = [22, 80, 443, 3306, 5432, 8080]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((str(ip), port))
                sock.close()
                
                if result == 0:
                    with self.lock:
                        if str(ip) not in self.active_hosts:
                            self.active_hosts.append(str(ip))
                            logger.info(f"✓ Found host: {ip} (port {port} open)")
                    return True
            except:
                pass
        
        return False
    
    def scan(self):
        """Scan entire network"""
        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            hosts = list(network.hosts())
            total_hosts = len(hosts)
            
            logger.info(f"🔍 Scanning {self.network_range} ({total_hosts} hosts)...")
            logger.info(f"Using {self.threads} threads")
            
            queue = Queue()
            for host in hosts:
                queue.put(host)
            
            def worker():
                while not queue.empty():
                    try:
                        ip = queue.get_nowait()
                        self.ping_host(ip)
                    except:
                        break
                    finally:
                        queue.task_done()
            
            threads = []
            start_time = time.time()
            
            for _ in range(min(self.threads, total_hosts)):
                t = threading.Thread(target=worker, daemon=True)
                t.start()
                threads.append(t)
            
            queue.join()
            
            for t in threads:
                t.join(timeout=1)
            
            elapsed = time.time() - start_time
            
            logger.info(f"\n✅ Scan complete!")
            logger.info(f"Found {len(self.active_hosts)} active hosts in {elapsed:.2f} seconds")
            
            return sorted(self.active_hosts)
        
        except ValueError as e:
            logger.error(f"Invalid network range: {str(e)}")
            return []


def get_local_network():
    """Get local network information"""
    try:
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Generate network range (assuming /24)
        parts = local_ip.split('.')
        network = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        
        return local_ip, network
    except:
        return None, None


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════╗
    ║    Network Discovery Scanner           ║
    ║    Scan your network for active hosts  ║
    ╚════════════════════════════════════════╝
    """)
    
    local_ip, default_network = get_local_network()
    
    if local_ip:
        print(f"📍 Local IP: {local_ip}")
        print(f"🌐 Default network: {default_network}\n")
    
    # Get user input
    network_input = input("Enter network range (CIDR, e.g., 192.168.1.0/24)\n> ").strip()
    
    if not network_input:
        if default_network:
            network_input = default_network
        else:
            print("❌ Please provide a valid network range")
            exit(1)
    
    threads_input = input("Number of threads (default 50):\n> ").strip()
    threads = int(threads_input) if threads_input else 50
    
    # Run scan
    scanner = NetworkDiscovery(network_input, threads)
    active_hosts = scanner.scan()
    
    if active_hosts:
        print("\n✅ Active Hosts Found:")
        print("=" * 50)
        for host in active_hosts:
            print(f"  • {host}")
        
        print("\n💡 Next steps:")
        print(f"   1. Copy these IPs to the Lab Scanner GUI")
        print(f"   2. Run individual full scans on each host")
        print(f"   3. Export results for network mapping")
    else:
        print("\n❌ No active hosts found on this network")
