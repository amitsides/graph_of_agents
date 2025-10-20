from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class HandoffType(Enum):
    """Types of handoff events in the A2A protocol."""
    TASK_ASSIGNMENT = "task_assignment"
    TASK_COMPLETION = "task_completion"
    TASK_ESCALATION = "task_escalation"
    INFORMATION_SHARE = "information_share"
    COLLABORATION_REQUEST = "collaboration_request"

@dataclass
class HandoffEvent:
    """Represents a handoff event between agents in the A2A protocol."""
    event_id: str
    handoff_type: HandoffType
    from_agent_id: str
    to_agent_id: str
    task_id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate the handoff event data."""
        if not self.event_id or not isinstance(self.event_id, str):
            raise ValueError("Event ID must be a non-empty string")
        if not isinstance(self.handoff_type, HandoffType):
            raise ValueError("Handoff type must be a HandoffType enum")
        if not self.from_agent_id or not isinstance(self.from_agent_id, str):
            raise ValueError("From agent ID must be a non-empty string")
        if not self.to_agent_id or not isinstance(self.to_agent_id, str):
            raise ValueError("To agent ID must be a non-empty string")
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the handoff event to a dictionary."""
        return {
            "event_id": self.event_id,
            "handoff_type": self.handoff_type.value,
            "from_agent_id": self.from_agent_id,
            "to_agent_id": self.to_agent_id,
            "task_id": self.task_id,
            "payload": self.payload,
            "message": self.message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata
        }

# Test with sample data
handoff_event_sample = HandoffEvent(
    event_id="event_001",
    handoff_type=HandoffType.TASK_ASSIGNMENT,
    from_agent_id="agent_001",
    to_agent_id="agent_002",
    task_id="task_001",
    payload={"priority": "high", "deadline": "2024-12-31"},
    message="Assigning data analysis task"
)

print("HandoffEvent created successfully:")
print(f"  Event ID: {handoff_event_sample.event_id}")
print(f"  Type: {handoff_event_sample.handoff_type.value}")
print(f"  From: {handoff_event_sample.from_agent_id}")
print(f"  To: {handoff_event_sample.to_agent_id}")
print(f"  Task ID: {handoff_event_sample.task_id}")
print(f"  Message: {handoff_event_sample.message}")
print(f"  Timestamp: {handoff_event_sample.timestamp}")
print(f"  Dict conversion: {handoff_event_sample.to_dict()}")