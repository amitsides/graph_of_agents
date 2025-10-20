from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

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
    metadata: Optional[dict] = None

class BaseAgent(ABC):
    """
    Base class for all agents in the ADK agent hierarchy.
    Provides lifecycle management, message handling, and basic agent functionality.
    """
    
    def __init__(self, agent_id: str, name: str, description: str = ""):
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name
            description: Description of agent's purpose
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.state = AgentState.CREATED
        self._message_queue = []
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    # Lifecycle methods
    def initialize(self) -> None:
        """Initialize the agent and prepare it for operation."""
        if self.state != AgentState.CREATED:
            raise RuntimeError(f"Cannot initialize agent in state: {self.state}")
        
        self._on_initialize()
        self.state = AgentState.INITIALIZED
        self._updated_at = datetime.now()
        print(f"Agent '{self.name}' ({self.agent_id}) initialized")
    
    def start(self) -> None:
        """Start the agent's execution."""
        if self.state not in [AgentState.INITIALIZED, AgentState.PAUSED]:
            raise RuntimeError(f"Cannot start agent in state: {self.state}")
        
        self._on_start()
        self.state = AgentState.RUNNING
        self._updated_at = datetime.now()
        print(f"Agent '{self.name}' ({self.agent_id}) started")
    
    def pause(self) -> None:
        """Pause the agent's execution."""
        if self.state != AgentState.RUNNING:
            raise RuntimeError(f"Cannot pause agent in state: {self.state}")
        
        self._on_pause()
        self.state = AgentState.PAUSED
        self._updated_at = datetime.now()
        print(f"Agent '{self.name}' ({self.agent_id}) paused")
    
    def stop(self) -> None:
        """Stop the agent's execution."""
        if self.state == AgentState.STOPPED:
            return
        
        self._on_stop()
        self.state = AgentState.STOPPED
        self._updated_at = datetime.now()
        print(f"Agent '{self.name}' ({self.agent_id}) stopped")
    
    def reset(self) -> None:
        """Reset the agent to its initial state."""
        self._on_reset()
        self.state = AgentState.CREATED
        self._message_queue.clear()
        self._updated_at = datetime.now()
        print(f"Agent '{self.name}' ({self.agent_id}) reset")
    
    # Message handling
    def send_message(self, message: AgentMessage) -> None:
        """Send a message to another agent or system."""
        self._on_send_message(message)
        print(f"Agent '{self.name}' sent message {message.message_id} to {message.recipient_id}")
    
    def receive_message(self, message: AgentMessage) -> None:
        """Receive a message from another agent or system."""
        self._message_queue.append(message)
        self._on_receive_message(message)
        print(f"Agent '{self.name}' received message {message.message_id} from {message.sender_id}")
    
    def process_messages(self) -> None:
        """Process all messages in the queue."""
        if not self._message_queue:
            return
        
        while self._message_queue:
            _msg = self._message_queue.pop(0)
            self._process_message(_msg)
    
    # Abstract methods for subclasses
    @abstractmethod
    def execute(self, task: Any) -> Any:
        """Execute a task. Must be implemented by subclasses."""
        pass
    
    # Hook methods for lifecycle events (can be overridden)
    def _on_initialize(self) -> None:
        """Hook called during initialization."""
        pass
    
    def _on_start(self) -> None:
        """Hook called when starting."""
        pass
    
    def _on_pause(self) -> None:
        """Hook called when pausing."""
        pass
    
    def _on_stop(self) -> None:
        """Hook called when stopping."""
        pass
    
    def _on_reset(self) -> None:
        """Hook called during reset."""
        pass
    
    def _on_send_message(self, message: AgentMessage) -> None:
        """Hook called when sending a message."""
        pass
    
    def _on_receive_message(self, message: AgentMessage) -> None:
        """Hook called when receiving a message."""
        pass
    
    def _process_message(self, message: AgentMessage) -> None:
        """Process a single message. Can be overridden."""
        pass
    
    # Utility methods
    def get_status(self) -> dict:
        """Get the current status of the agent."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "queue_size": len(self._message_queue),
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"BaseAgent(id={self.agent_id}, name={self.name}, state={self.state.value})"

print("BaseAgent class created successfully")
print(f"  - Lifecycle states: {[s.value for s in AgentState]}")
print(f"  - Key methods: initialize(), start(), pause(), stop(), reset()")
print(f"  - Message handling: send_message(), receive_message(), process_messages()")
print(f"  - Abstract method: execute() must be implemented by subclasses")
