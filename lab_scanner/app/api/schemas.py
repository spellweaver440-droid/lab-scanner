"""
API Response Schemas
Pydantic models for request/response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PortInfo(BaseModel):
    """Port information"""
    port: int = Field(..., description="Port number")
    service: str = Field(default="Unknown", description="Service name")
    banner: Optional[str] = Field(None, description="Service banner")
    status: str = Field(default="open", description="Port status")


class ScanRequest(BaseModel):
    """Scan request parameters"""
    target: str = Field(..., description="Target IP or hostname")
    ports: Optional[str] = Field("1-1024", description="Port range (e.g., '1-1024' or '22,80,443')")
    threads: Optional[int] = Field(100, description="Number of threads")
    timeout: Optional[int] = Field(2, description="Connection timeout in seconds")
    scan_type: Optional[str] = Field("full", description="Scan type: full, quick, web")


class PortScanResponse(BaseModel):
    """Port scan response"""
    target: str
    total_ports_scanned: int
    open_ports: List[int]
    closed_ports: int
    status: str


class ServiceInfo(BaseModel):
    """Service detection info"""
    port: int
    service: str
    banner: str
    status: str


class Vulnerability(BaseModel):
    """Vulnerability information"""
    name: str = Field(..., description="Vulnerability name")
    severity: str = Field(..., description="Severity level")
    description: str
    port: int
    cve: Optional[str] = None
    score: float = 0.0


class WebVulnerability(BaseModel):
    """Web vulnerability info"""
    check: str
    severity: Optional[str] = None
    status: str
    details: Optional[Dict[str, Any]] = None


class ScanReport(BaseModel):
    """Complete scan report"""
    target: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    scan_type: str
    status: str
    
    # Port scan results
    open_ports: List[int]
    services: List[ServiceInfo]
    
    # Vulnerabilities
    vulnerabilities: List[Vulnerability]
    vulnerability_count: int
    
    # Risk assessment
    overall_risk_level: str
    average_risk_score: float
    max_risk_score: float


class ScanHistoryItem(BaseModel):
    """Scan history item"""
    id: int
    target: str
    scan_type: str
    timestamp: datetime
    vulnerability_count: int
    overall_risk_level: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
