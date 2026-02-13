"""
Distributed Agent System (Phase 4)
Agents poll master for tasks and execute scans
"""
import requests
import time
from typing import Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ScanTask:
    """Scan task for agents"""
    task_id: str
    target: str
    ports: str
    scan_type: str
    priority: int = 0
    timestamp: str = ""


class ScanAgent:
    """Distributed scan agent - executes tasks from master"""
    
    def __init__(self, agent_id: str, master_url: str = "http://localhost:8000"):
        """
        Initialize scan agent
        
        Args:
            agent_id: Unique agent identifier
            master_url: Master API URL
        """
        self.agent_id = agent_id
        self.master_url = master_url.rstrip('/')
        self.active = False
        self.current_task = None

    def register(self) -> bool:
        """Register agent with master"""
        try:
            response = requests.post(
                f"{self.master_url}/agents/register",
                json={
                    "agent_id": self.agent_id,
                    "status": "online",
                    "capabilities": ["port_scan", "service_detection", "web_scan"]
                },
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Agent {self.agent_id} registered with master")
                self.active = True
                return True
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
        return False

    def get_task(self) -> Optional[ScanTask]:
        """Poll master for scan task"""
        try:
            response = requests.get(
                f"{self.master_url}/agents/task/{self.agent_id}",
                timeout=5
            )
            if response.status_code == 200:
                task_data = response.json()
                if task_data:
                    return ScanTask(**task_data)
        except Exception as e:
            logger.error(f"Error getting task: {str(e)}")
        return None

    def execute_task(self, task: ScanTask) -> Dict:
        """Execute scan task"""
        logger.info(f"Executing task {task.task_id} on {task.target}")
        
        try:
            # Call back to master API to perform scan
            response = requests.post(
                f"{self.master_url}/scan/{task.scan_type}",
                json={
                    "target": task.target,
                    "ports": task.ports
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
        
        return {"error": "Task execution failed"}

    def submit_result(self, task_id: str, result: Dict) -> bool:
        """Submit task result back to master"""
        try:
            response = requests.post(
                f"{self.master_url}/agents/result/{self.agent_id}",
                json={
                    "task_id": task_id,
                    "result": result,
                    "status": "completed"
                },
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error submitting result: {str(e)}")
        return False

    def start_polling(self, poll_interval: int = 5):
        """Start polling master for tasks"""
        logger.info(f"Agent {self.agent_id} starting polling loop")
        
        if not self.register():
            logger.error("Failed to register agent")
            return
        
        while self.active:
            try:
                task = self.get_task()
                
                if task:
                    self.current_task = task
                    result = self.execute_task(task)
                    self.submit_result(task.task_id, result)
                    self.current_task = None
                
                time.sleep(poll_interval)
                
            except KeyboardInterrupt:
                logger.info("Agent stopping")
                self.active = False
            except Exception as e:
                logger.error(f"Agent error: {str(e)}")
                time.sleep(poll_interval)

    def stop(self):
        """Stop agent"""
        self.active = False
        logger.info(f"Agent {self.agent_id} stopped")


class MasterCoordinator:
    """Master coordinator for distributed agents"""
    
    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.tasks: Dict[str, ScanTask] = {}
        self.results: Dict[str, Dict] = {}

    def register_agent(self, agent_id: str, capabilities: list) -> bool:
        """Register new agent"""
        self.agents[agent_id] = {
            "status": "online",
            "capabilities": capabilities,
            "last_seen": time.time()
        }
        logger.info(f"Agent registered: {agent_id}")
        return True

    def assign_task(self, task: ScanTask, agent_id: str = None) -> str:
        """Assign task to agent"""
        if agent_id:
            self.tasks[task.task_id] = (task, agent_id)
            logger.info(f"Task {task.task_id} assigned to {agent_id}")
            return task.task_id
        
        # Find available agent
        for aid, info in self.agents.items():
            if info["status"] == "online":
                self.tasks[task.task_id] = (task, aid)
                logger.info(f"Task {task.task_id} assigned to {aid}")
                return task.task_id
        
        logger.warning("No available agents for task")
        return None

    def store_result(self, task_id: str, result: Dict):
        """Store task result"""
        self.results[task_id] = result
        logger.info(f"Result stored for task {task_id}")

    def get_agent_status(self) -> Dict:
        """Get all agent statuses"""
        return {
            "total_agents": len(self.agents),
            "agents": self.agents
        }
