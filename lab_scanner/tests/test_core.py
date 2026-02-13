"""
Lab Scanner Tests
Unit and integration tests
"""
import pytest
from app.core.port_scanner import PortScanner
from app.core.service_detector import ServiceDetector, OSFingerprint
from app.core.vuln_engine import VulnerabilityEngine


class TestPortScanner:
    """Test port scanning functionality"""
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        scanner = PortScanner("127.0.0.1", [22, 80, 443])
        assert scanner.target == "127.0.0.1"
        assert scanner.ports == [22, 80, 443]
    
    def test_scan_port_closed(self):
        """Test scanning closed port"""
        scanner = PortScanner("127.0.0.1", [9999])
        result = scanner.scan_port(9999)
        assert result == False


class TestServiceDetector:
    """Test service detection"""
    
    def test_service_detection_init(self):
        """Test service detector initialization"""
        detector = ServiceDetector("192.168.1.1")
        assert detector.target == "192.168.1.1"
    
    def test_port_service_mapping(self):
        """Test port to service mapping"""
        assert ServiceDetector.PORT_SERVICE_MAP.get(22) == "SSH"
        assert ServiceDetector.PORT_SERVICE_MAP.get(80) == "HTTP"
        assert ServiceDetector.PORT_SERVICE_MAP.get(443) == "HTTPS"


class TestVulnerabilityEngine:
    """Test vulnerability analysis"""
    
    def test_cvss_scoring(self):
        """Test CVSS score calculation"""
        score = VulnerabilityEngine.calculate_risk_score("High")
        assert score == 7.0
    
    def test_vulnerability_identification(self):
        """Test vulnerability identification"""
        vulns = VulnerabilityEngine.identify_vulnerabilities("SSH", 22, "OpenSSH_7.4")
        assert len(vulns) > 0
        assert any(v["port"] == 22 for v in vulns)


class TestOSFingerprint:
    """Test OS fingerprinting"""
    
    def test_windows_fingerprint(self):
        """Test Windows OS detection"""
        services = [
            {"port": 445, "service": "SMB", "banner": "N/A"}
        ]
        os_name = OSFingerprint.fingerprint(services)
        assert os_name == "Windows"
    
    def test_linux_fingerprint(self):
        """Test Linux OS detection"""
        services = [
            {"port": 22, "service": "SSH", "banner": "OpenSSH"}
        ]
        os_name = OSFingerprint.fingerprint(services)
        assert os_name == "Linux/Unix"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
