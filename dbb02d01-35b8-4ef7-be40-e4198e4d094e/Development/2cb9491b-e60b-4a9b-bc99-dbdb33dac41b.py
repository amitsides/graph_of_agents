from typing import Optional, Dict, Any
from dataclasses import dataclass
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
class HandoffEventCopy:
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

# Test validation for HandoffEvent
print("=== Testing HandoffEvent Validation ===")
try:
    _invalid_event = HandoffEventCopy(
        event_id="", 
        handoff_type=HandoffType.TASK_ASSIGNMENT,
        from_agent_id="agent1",
        to_agent_id="agent2"
    )
    print("❌ FAILED: Empty event_id should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty event_id validation - {e}")

try:
    _invalid_event = HandoffEventCopy(
        event_id="123",
        handoff_type=HandoffType.TASK_ASSIGNMENT,
        from_agent_id="",
        to_agent_id="agent2"
    )
    print("❌ FAILED: Empty from_agent_id should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty from_agent_id validation - {e}")

print("✅ HandoffEvent validation: Complete")