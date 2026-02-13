#!/usr/bin/env python3
"""
Distributed Agent Startup Example
Run this on machines that will perform distributed scans
"""
import sys
from agents.agent import ScanAgent

if __name__ == "__main__":
    # Create agent
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "agent-01"
    master_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║  Lab Scanner - Distributed Agent        ║
    ║  Agent ID:  {agent_id:26s}║
    ║  Master:    {master_url:26s}║
    ╚══════════════════════════════════════════╝
    """)
    
    agent = ScanAgent(agent_id, master_url)
    
    try:
        agent.start_polling(poll_interval=5)
    except KeyboardInterrupt:
        print("\nAgent shutting down...")
        agent.stop()
