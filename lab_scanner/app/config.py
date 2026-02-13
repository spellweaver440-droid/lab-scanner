"""
Configuration Module
Centralized settings for the lab scanner
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_TITLE: str = "Lab Scanner API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Enterprise-style vulnerability scanner"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lab_scanner.db")
    
    # Scanning
    DEFAULT_THREADS: int = 100
    DEFAULT_TIMEOUT: int = 2
    MAX_PORTS: int = 65535
    DEFAULT_PORT_RANGE: str = "1-1024"
    
    # Web Scanning
    WEB_SCAN_TIMEOUT: int = 5
    
    # Plugin System
    PLUGIN_DIR: str = os.path.join(os.path.dirname(__file__), 'plugins')
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
