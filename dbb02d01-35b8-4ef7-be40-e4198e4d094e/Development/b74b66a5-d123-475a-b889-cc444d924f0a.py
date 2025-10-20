from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Import necessary classes
class AgentState(Enum):
    """Lifecycle states for agents."""
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Represents a message between agents or for internal processing."""
    message_id: str
    sender_id: str
    recipient_id: str
    content: dict
    message_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = None

class OrchestrationAgent(BaseAgent):
    """
    Orchestration agent that extends BaseAgent with multi-agent coordination capabilities.
    Can manage multiple sub-agents, delegate tasks, and coordinate workflows.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str = "",
        max_concurrent_tasks: int = 5
    ):
        """
        Initialize the orchestration agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name
            description: Description of agent's purpose
            max_concurrent_tasks: Maximum number of concurrent tasks
        """
        super().__init__(agent_id, name, description)
        self.max_concurrent_tasks = max_concurrent_tasks
        self._sub_agents: dict = {}
        self._active_tasks: dict = {}
        self._completed_tasks: list = []
        self._task_queue = []
    
    def execute(self, task: Any) -> dict:
        """
        Execute a task by orchestrating sub-agents.
        
        Args:
            task: The task to execute
            
        Returns:
            Dict containing the execution result
        """
        if self.state != AgentState.RUNNING:
            raise RuntimeError(f"Cannot execute task when agent is in state: {self.state}")
        
        # Convert task to dict if needed
        if isinstance(task, str):
            _orch_task_dict = {"task_id": str(len(self._completed_tasks)), "description": task}
        elif isinstance(task, dict):
            _orch_task_dict = task
        else:
            _orch_task_dict = {"task_id": str(len(self._completed_tasks)), "description": str(task)}
        
        # Process the task
        _orch_task_id = _orch_task_dict.get("task_id", str(len(self._completed_tasks)))
        
        # Simulate orchestration logic
        _orch_result = self._orchestrate_task(_orch_task_dict)
        
        # Track completed task
        self._completed_tasks.append({
            "task_id": _orch_task_id,
            "task": _orch_task_dict,
            "result": _orch_result,
            "completed_at": datetime.now().isoformat()
        })
        
        print(f"OrchestrationAgent '{self.name}' executed task {_orch_task_id}")
        return _orch_result
    
    def _orchestrate_task(self, task: dict) -> dict:
        """
        Orchestrate a task across sub-agents.
        
        Args:
            task: The task to orchestrate
            
        Returns:
            Dict with orchestration result
        """
        _orch_task_id = task.get("task_id", "unknown")
        
        # Simulate delegation to sub-agents
        if self._sub_agents:
            _orch_assigned_agent = list(self._sub_agents.keys())[0]
            _orch_simulated_result = f"Task {_orch_task_id} delegated to agent {_orch_assigned_agent}"
        else:
            _orch_simulated_result = f"Task {_orch_task_id} executed directly (no sub-agents available)"
        
        return {
            "success": True,
            "task_id": _orch_task_id,
            "result": _orch_simulated_result,
            "sub_agents_used": len(self._sub_agents),
            "total_completed": len(self._completed_tasks) + 1
        }
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register a sub-agent for orchestration.
        
        Args:
            agent: The agent to register
        """
        self._sub_agents[agent.agent_id] = agent
        print(f"OrchestrationAgent '{self.name}' registered sub-agent '{agent.name}' ({agent.agent_id})")
    
    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister a sub-agent.
        
        Args:
            agent_id: ID of the agent to unregister
        """
        if agent_id in self._sub_agents:
            _removed_agent = self._sub_agents.pop(agent_id)
            print(f"OrchestrationAgent '{self.name}' unregistered sub-agent {agent_id}")
        else:
            print(f"OrchestrationAgent '{self.name}' could not find sub-agent {agent_id}")
    
    def get_sub_agents(self) -> list:
        """Get list of registered sub-agents."""
        return list(self._sub_agents.values())
    
    def delegate_task(self, task: dict, agent_id: str) -> dict:
        """
        Delegate a task to a specific sub-agent.
        
        Args:
            task: The task to delegate
            agent_id: ID of the sub-agent to delegate to
            
        Returns:
            Result of the delegation
        """
        if agent_id not in self._sub_agents:
            return {"success": False, "error": f"Agent {agent_id} not found"}
        
        _target_agent = self._sub_agents[agent_id]
        _orch_delegation_result = {
            "success": True,
            "delegated_to": agent_id,
            "task": task,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"OrchestrationAgent '{self.name}' delegated task to agent {agent_id}")
        return _orch_delegation_result
    
    def get_task_status(self, task_id: str) -> dict:
        """Get status of a specific task."""
        # Check active tasks
        if task_id in self._active_tasks:
            return {"status": "active", "task": self._active_tasks[task_id]}
        
        # Check completed tasks
        for _completed_task in self._completed_tasks:
            if _completed_task.get("task_id") == task_id:
                return {"status": "completed", "task": _completed_task}
        
        return None
    
    def _on_reset(self) -> None:
        """Hook called during reset."""
        super()._on_reset()
        self._active_tasks.clear()
        self._completed_tasks.clear()
        self._task_queue.clear()
    
    def get_status(self) -> dict:
        """Get the current status including orchestration-specific info."""
        _orch_status_dict = super().get_status()
        _orch_status_dict.update({
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "sub_agents_count": len(self._sub_agents),
            "active_tasks_count": len(self._active_tasks),
            "completed_tasks_count": len(self._completed_tasks),
            "queued_tasks_count": len(self._task_queue)
        })
        return _orch_status_dict
    
    def __repr__(self) -> str:
        return f"OrchestrationAgent(id={self.agent_id}, name={self.name}, sub_agents={len(self._sub_agents)}, state={self.state.value})"

print("OrchestrationAgent class created successfully")
print(f"  - Extends BaseAgent with orchestration capabilities")
print(f"  - Key methods: register_agent(), delegate_task(), get_sub_agents()")
print(f"  - Tracks: active_tasks, completed_tasks, task_queue")
print(f"  - Coordinates multiple sub-agents for complex workflows")
