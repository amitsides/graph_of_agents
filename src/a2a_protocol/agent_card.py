from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class AgentCard:
    """Represents an agent's identity and capabilities in the A2A protocol."""
    agent_id: str
    name: str
    description: str
    skills: List[Any]  # Will be List[AgentSkill] when used together
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

# Test with sample data
agent_card_sample = AgentCard(
    agent_id="agent_001",
    name="Data Analyst Agent",
    description="Specialized in data analysis and visualization",
    skills=[skill_sample],  # Using skill_sample from previous block
    version="1.0.0",
    metadata={"team": "analytics", "priority": "high"}
)

print("AgentCard created successfully:")
print(f"  Agent ID: {agent_card_sample.agent_id}")
print(f"  Name: {agent_card_sample.name}")
print(f"  Description: {agent_card_sample.description}")
print(f"  Skills: {len(agent_card_sample.skills)} skill(s)")
print(f"  Version: {agent_card_sample.version}")
print(f"  Created: {agent_card_sample.created_at}")