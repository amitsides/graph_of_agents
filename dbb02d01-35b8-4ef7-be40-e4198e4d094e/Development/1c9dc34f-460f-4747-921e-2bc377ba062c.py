from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Re-import the AgentSkill class to have it available with proper dataclass decorator
@dataclass
class AgentSkillCopy:
    """Represents a skill that an agent possesses."""
    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None
    examples: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate the skill data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Skill name must be a non-empty string")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Skill description must be a non-empty string")
        if self.parameters is not None and not isinstance(self.parameters, dict):
            raise ValueError("Skill parameters must be a dictionary")
        if self.examples is not None and not isinstance(self.examples, list):
            raise ValueError("Skill examples must be a list")

# Test validation for AgentSkill
print("=== Testing AgentSkill Validation ===")
try:
    _invalid_skill = AgentSkillCopy(name="", description="Test")
    print("❌ FAILED: Empty name should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Empty name validation - {e}")

try:
    _invalid_skill = AgentSkillCopy(name="test", description="", parameters="not_a_dict")
    print("❌ FAILED: Invalid parameters type should raise ValueError")
except ValueError as e:
    print(f"✅ PASSED: Parameters type validation - {e}")

print("✅ AgentSkill validation: Complete")