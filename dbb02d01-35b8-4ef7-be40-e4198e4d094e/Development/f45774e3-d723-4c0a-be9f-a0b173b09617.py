from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Re-define AgentCard for validation testing
@dataclass
class AgentCardCopy:
    """Represents an agent's identity and capabilities in the A2A protocol."""
    agent_id: str
    name: str
    description: str
    skills: List[Any]
    version: str = "1.0.0"
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate the agent card data."""
        if not self.agent_id or not isinstance(self.agent_id, str):
            raise ValueError("Agent ID must be a non-empty string")
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Agent name must be a non-empty string")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Agent description must be a non-empty string")
        if not isinstance(self.skills, list):
            raise ValueError("Skills must be a list")
        if not isinstance(self.version, str):
            raise ValueError("Version must be a string")
        if self.created_at is None:
            self.created_at = datetime.now()

# Test validation for AgentCard
print("=== Testing AgentCard Validation ===")
try:
    _invalid_card = AgentCardCopy(agent_id="", name="Test", description="Test", skills=[])
    print("❌ FAILED: Empty agent_id should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty agent_id validation - {e}")

try:
    _invalid_card = AgentCardCopy(agent_id="123", name="Test", description="Test", skills="not_a_list")
    print("❌ FAILED: Invalid skills type should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Skills type validation - {e}")

print("✅ AgentCard validation: Complete")