from dataclasses import dataclass

@dataclass
class AgentSkill:
    """Represents a skill that an agent possesses."""
    name: str
    description: str
    parameters: dict = None
    examples: list = None
    
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

# Test with sample data
skill_sample = AgentSkill(
    name="data_analysis",
    description="Analyze datasets and generate insights",
    parameters={"data_types": ["csv", "json"], "max_size_mb": 100},
    examples=["Analyze sales data", "Generate summary statistics"]
)

print("AgentSkill created successfully:")
print(f"  Name: {skill_sample.name}")
print(f"  Description: {skill_sample.description}")
print(f"  Parameters: {skill_sample.parameters}")
print(f"  Examples: {skill_sample.examples}")

# Ensure class has fields defined
print(f"  Fields: {AgentSkill.__dataclass_fields__.keys()}")
