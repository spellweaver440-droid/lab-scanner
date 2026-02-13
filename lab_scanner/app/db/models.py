"""
Database Models
SQLAlchemy ORM models for storing scan results
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ScanRecord(Base):
    """Scan history record"""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, index=True)
    scan_type = Column(String)  # full, port, web, service
    status = Column(String)  # completed, running, failed
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Results
    open_ports = Column(Text)  # JSON string
    services_found = Column(Integer, default=0)
    vulnerabilities_found = Column(Integer, default=0)
    
    # Risk assessment
    overall_risk_level = Column(String)
    average_risk_score = Column(Float, default=0.0)
    max_risk_score = Column(Float, default=0.0)
    
    # Metadata
    duration_seconds = Column(Integer)
    notes = Column(Text, nullable=True)


class Vulnerability(Base):
    """Vulnerability record"""
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer)
    target = Column(String, index=True)
    port = Column(Integer)
    service = Column(String)
    name = Column(String)
    severity = Column(String)  # Critical, High, Medium, Low, Info
    description = Column(Text)
    cve = Column(String, nullable=True)
    cvss_score = Column(Float)
    discovered_at = Column(DateTime, default=datetime.utcnow)


class Agent(Base):
    """Distributed agent record"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, unique=True, index=True)
    status = Column(String)  # online, offline, busy
    capabilities = Column(Text)  # JSON string
    last_seen = Column(DateTime, default=datetime.utcnow)
    scans_completed = Column(Integer, default=0)
    registered_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    """Scan task for distributed execution"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    agent_id = Column(String, nullable=True)
    target = Column(String)
    scan_type = Column(String)
    status = Column(String)  # pending, assigned, running, completed, failed
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)
