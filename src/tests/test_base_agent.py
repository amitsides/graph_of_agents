from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# Import agent classes
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
    content: Dict[str, Any]
    message_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

# Test BaseAgent instantiation and lifecycle
print("=== Testing BaseAgent ===")
print()

# Create a concrete implementation for testing
class TestAgent(BaseAgent):
    """Test implementation of BaseAgent."""
    def execute(self, task):
        return {"result": f"Executed: {task}"}

# Create and test agent
base_test_agent = TestAgent(
    agent_id="test_001",
    name="Test Agent",
    description="A test agent for validation"
)

print(f"Created: {base_test_agent}")
print(f"Status: {base_test_agent.get_status()}")
print()

# Test lifecycle
print("Testing lifecycle methods:")
base_test_agent.initialize()
print(f"  State after initialize: {base_test_agent.state.value}")

base_test_agent.start()
print(f"  State after start: {base_test_agent.state.value}")

# Test execution
base_execution_result = base_test_agent.execute("Sample task")
print(f"  Execution result: {base_execution_result}")

base_test_agent.pause()
print(f"  State after pause: {base_test_agent.state.value}")

base_test_agent.start()  # Resume
print(f"  State after resume: {base_test_agent.state.value}")

base_test_agent.stop()
print(f"  State after stop: {base_test_agent.state.value}")

base_test_agent.reset()
print(f"  State after reset: {base_test_agent.state.value}")
print()

# Test message handling
print("Testing message handling:")
base_test_message = AgentMessage(
    message_id="msg_001",
    sender_id="agent_001",
    recipient_id="test_001",
    content={"data": "test message"},
    message_type="info"
)

base_test_agent.receive_message(base_test_message)
base_test_agent.send_message(base_test_message)
print(f"  Message queue size: {len(base_test_agent._message_queue)}")
print()

print("✅ BaseAgent tests completed successfully!")
print(f"Final status: {base_test_agent.get_status()}")