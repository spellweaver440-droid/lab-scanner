"""
API Routes
RESTful endpoints for scanning operations
"""
from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime
from ..core.port_scanner import PortScanner
from ..core.service_detector import ServiceDetector, OSFingerprint
from ..core.web_scanner import WebScanner
from ..core.vuln_engine import VulnerabilityEngine
from ..core.network_scanner import NetworkScanner
from ..plugins.plugin_manager import PluginManager
from .schemas import (
    ScanRequest, ScanReport, PortScanResponse,
    ServiceInfo, Vulnerability, HealthResponse
)
from ..config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Global plugin manager
plugin_manager = None


def init_plugins():
    """Initialize plugin manager"""
    global plugin_manager
    if plugin_manager is None:
        plugin_manager = PluginManager(settings.PLUGIN_DIR)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow()
    }


@router.post("/scan/port", response_model=PortScanResponse)
async def port_scan(request: ScanRequest):
    """Execute port scan on target"""
    try:
        # Parse ports
        if '-' in request.ports:
            start, end = map(int, request.ports.split('-'))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p.strip()) for p in request.ports.split(',')]
        
        logger.info(f"Starting port scan on {request.target} ({len(ports)} ports)")
        
        scanner = PortScanner(
            target=request.target,
            ports=ports,
            threads=request.threads,
            timeout=request.timeout
        )
        
        results = scanner.run()
        return results
        
    except Exception as e:
        logger.error(f"Port scan error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scan/services")
async def service_scan(target: str = Query(...), ports: str = Query("22,80,443")):
    """Detect services on open ports"""
    try:
        port_list = [int(p.strip()) for p in ports.split(',')]
        
        detector = ServiceDetector(target)
        services = detector.detect_services(port_list)
        
        return {
            "target": target,
            "services": services,
            "count": len(services)
        }
        
    except Exception as e:
        logger.error(f"Service detection error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scan/web")
async def web_scan(target: str = Query(...), port: int = Query(80)):
    """Scan web server for vulnerabilities"""
    try:
        scanner = WebScanner(target, timeout=settings.WEB_SCAN_TIMEOUT)
        results = scanner.scan()
        
        return {
            "target": target,
            "port": port,
            "checks": results,
            "total_checks": len(results)
        }
        
    except Exception as e:
        logger.error(f"Web scan error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scan/full", response_model=ScanReport)
async def full_scan(request: ScanRequest):
    """Execute comprehensive vulnerability scan"""
    try:
        logger.info(f"Starting full scan on {request.target}")
        
        # Step 1: Port Scan
        ports = list(range(1, 1025))
        port_scanner = PortScanner(
            target=request.target,
            ports=ports,
            threads=request.threads,
            timeout=request.timeout
        )
        port_results = port_scanner.run()
        open_ports = port_results["open_ports"]
        
        # Step 2: Service Detection
        detector = ServiceDetector(request.target)
        services = detector.detect_services(open_ports)
        service_list = [
            ServiceInfo(
                port=s["port"],
                service=s["service"],
                banner=s.get("banner", "N/A"),
                status=s.get("status", "open")
            )
            for s in services
        ]
        
        # Step 3: OS Fingerprinting
        os_name = OSFingerprint.fingerprint(services)
        
        # Step 4: Vulnerability Analysis
        scan_data = {
            "target": request.target,
            "services": services
        }
        vuln_report = VulnerabilityEngine.generate_report(scan_data)
        
        vulnerabilities = [
            Vulnerability(
                name=v["name"],
                severity=v["severity"],
                description=v.get("description", ""),
                port=v.get("port", 0),
                cve=v.get("cve", "N/A"),
                score=v.get("score", 0.0)
            )
            for v in vuln_report.get("vulnerabilities", [])
        ]
        
        # Step 5: Run plugins
        init_plugins()
        plugin_results = []
        for service in services[:5]:  # Run on first 5 to keep demo fast
            for port in open_ports[:5]:
                if plugin_manager:
                    plugin_results.extend(
                        plugin_manager.run_all_plugins(
                            request.target,
                            port,
                            service.get("service", "")
                        )
                    )
        
        return ScanReport(
            target=request.target,
            timestamp=datetime.utcnow(),
            scan_type="full",
            status="completed",
            open_ports=open_ports,
            services=service_list,
            vulnerabilities=vulnerabilities,
            vulnerability_count=len(vulnerabilities),
            overall_risk_level=vuln_report.get("overall_risk_level", "Unknown"),
            average_risk_score=vuln_report.get("average_risk_score", 0.0),
            max_risk_score=vuln_report.get("max_risk_score", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Full scan error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/plugins/list")
async def list_plugins():
    """List all available plugins"""
    init_plugins()
    
    if not plugin_manager:
        return {"plugins": [], "count": 0}
    
    plugins = []
    for plugin_name in plugin_manager.list_plugins():
        plugin_class = plugin_manager.get_plugin(plugin_name)
        plugins.append({
            "name": plugin_name,
            "description": getattr(plugin_class, 'description', ''),
            "severity": getattr(plugin_class, 'severity', 'Info'),
            "version": getattr(plugin_class, 'version', '1.0.0'),
        })
    
    return {
        "plugins": plugins,
        "count": len(plugins)
    }


@router.post("/discover/network")
async def network_discovery(
    network_range: str = Query(..., description="Network in CIDR notation (e.g., 192.168.1.0/24)"),
    threads: int = Query(50, description="Number of discovery threads")
):
    """Discover active hosts on a network"""
    try:
        logger.info(f"Starting network discovery on {network_range}")
        
        scanner = NetworkScanner(network_range, threads=threads, timeout=1)
        active_hosts = scanner.discover_hosts()
        
        logger.info(f"Found {len(active_hosts)} active hosts")
        
        return {
            "network": network_range,
            "active_hosts": active_hosts,
            "count": len(active_hosts),
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Network discovery error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Network discovery error: {str(e)}")


@router.post("/scan/batch")
async def batch_scan(
    targets: List[str] = Query(..., description="List of target IPs"),
    scan_type: str = Query("port", description="Scan type: port, service, web, full")
):
    """Scan multiple targets in sequence"""
    try:
        logger.info(f"Starting batch scan on {len(targets)} targets")
        
        results = []
        for target in targets:
            try:
                logger.info(f"Scanning target: {target}")
                
                if scan_type == "port":
                    scanner = PortScanner(target, list(range(1, 1025)), threads=100, timeout=2)
                    result = scanner.run()
                elif scan_type == "service":
                    detector = ServiceDetector(target)
                    result = {"target": target, "services": detector.detect_services([22, 80, 443])}
                else:
                    result = {"target": target, "status": "skipped"}
                
                results.append(result)
            except Exception as e:
                logger.error(f"Error scanning {target}: {str(e)}")
                results.append({"target": target, "error": str(e)})
        
        return {
            "total_targets": len(targets),
            "scanned": len([r for r in results if "error" not in r]),
            "results": results,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Batch scan error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/plugins/run")
async def run_plugin(
    plugin_name: str = Query(...),
    target: str = Query(...),
    port: int = Query(80),
    service: Optional[str] = Query(None)
):
    """Execute a specific plugin"""
    init_plugins()
    
    if not plugin_manager:
        raise HTTPException(status_code=500, detail="Plugin manager not initialized")
    
    result = plugin_manager.run_plugin(plugin_name, target, port, service or "")
    return result
